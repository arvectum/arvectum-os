from __future__ import annotations

from pathlib import Path
import unittest

from arvectum_os_ref.authority_safe_ux import (
    AuthoritySafeActionLabel,
    AuthoritySafeUxDecision,
    AuthoritySafeUxState,
    consume_current_source_authorization,
)
from arvectum_os_ref.canonical_inspection import CurrentSourceAuthorization
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import WorkspaceShellState, open_workspace_shell


REFERENCE_ROOT = Path(__file__).parents[1]
PLATFORM_ROOT = REFERENCE_ROOT / "arvectum_os_ref"
PRODUCT_ROOT = REFERENCE_ROOT / "bounded_product_ref"


class R12M4WorkspaceHardeningTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(
            Identity("organization", "org-r12", "platform")
        )
        self.actor = ActorContext(
            Principal(Identity("principal", "operator-r12", "platform")),
            self.organization,
        )
        workspace = open_workspace_shell(self.actor)
        self.assertIsInstance(workspace, WorkspaceShellState)
        self.workspace = workspace
        self.subject = Identity("record-subject", "subject-r12", "platform")
        self.decision_v1 = Identity(
            "authorization-decision-version", "r12-v1", "platform"
        )
        self.decision_v2 = Identity(
            "authorization-decision-version", "r12-v2", "platform"
        )

    def _allow(self, version: Identity) -> CurrentSourceAuthorization:
        return CurrentSourceAuthorization(
            organization=self.organization,
            actor_actual_principal_id=self.actor.actual_principal.principal_id,
            resource_subject_id=self.subject,
            decision_version_id=version,
            allowed=True,
        )

    def test_replaced_authorization_cannot_self_advance_stale_presentation(self) -> None:
        initial = consume_current_source_authorization(
            workspace=self.workspace,
            resource_subject_id=self.subject,
            source_authorizations=(self._allow(self.decision_v1),),
            allow_derived_preview=True,
        )
        self.assertEqual(initial.state, AuthoritySafeUxState.AVAILABLE)
        self.assertEqual(
            initial.source_authorization_decision_version_id, self.decision_v1
        )

        replaced = consume_current_source_authorization(
            workspace=self.workspace,
            resource_subject_id=self.subject,
            source_authorizations=(self._allow(self.decision_v2),),
            expected_decision_version_id=initial.source_authorization_decision_version_id,
            allow_derived_preview=True,
        )
        self.assertEqual(
            replaced.state, AuthoritySafeUxState.REINSPECTION_REQUIRED
        )
        self.assertEqual(replaced.action_label, AuthoritySafeActionLabel.REINSPECT)
        self.assertEqual(
            replaced.source_authorization_decision_version_id, self.decision_v1
        )
        self.assertNotEqual(
            replaced.source_authorization_decision_version_id, self.decision_v2
        )
        self.assertFalse(replaced.governed_content_visible)
        self.assertFalse(replaced.protected_count_visible)
        self.assertFalse(replaced.derived_preview_visible)

        repeated_from_blocked_state = consume_current_source_authorization(
            workspace=self.workspace,
            resource_subject_id=self.subject,
            source_authorizations=(self._allow(self.decision_v2),),
            expected_decision_version_id=(
                replaced.source_authorization_decision_version_id
            ),
            allow_derived_preview=True,
        )
        self.assertEqual(
            repeated_from_blocked_state.state,
            AuthoritySafeUxState.REINSPECTION_REQUIRED,
        )
        self.assertEqual(
            repeated_from_blocked_state.source_authorization_decision_version_id,
            self.decision_v1,
        )
        self.assertFalse(repeated_from_blocked_state.governed_content_visible)

    def test_authority_safe_decision_rejects_inconsistent_fail_open_states(self) -> None:
        with self.assertRaises(ValueError):
            AuthoritySafeUxDecision(
                state=AuthoritySafeUxState.AVAILABLE,
                action_label=AuthoritySafeActionLabel.REQUEST_ACTION,
                source_authorization_decision_version_id=None,
                governed_content_visible=True,
            )

        with self.assertRaises(ValueError):
            AuthoritySafeUxDecision(
                state=AuthoritySafeUxState.REINSPECTION_REQUIRED,
                action_label=AuthoritySafeActionLabel.REQUEST_ACTION,
                source_authorization_decision_version_id=self.decision_v1,
                governed_content_visible=False,
            )

        with self.assertRaises(ValueError):
            AuthoritySafeUxDecision(
                state=AuthoritySafeUxState.NOT_AVAILABLE,
                action_label=AuthoritySafeActionLabel.UNAVAILABLE,
                source_authorization_decision_version_id=self.decision_v1,
                governed_content_visible=False,
            )

        with self.assertRaises(ValueError):
            AuthoritySafeUxDecision(
                state=AuthoritySafeUxState.REINSPECTION_REQUIRED,
                action_label=AuthoritySafeActionLabel.REINSPECT,
                source_authorization_decision_version_id=self.decision_v1,
                governed_content_visible=True,
            )

    def test_narrow_decision_consumer_does_not_replace_semantic_owner_controls(self) -> None:
        reviewed = {
            "provenance_inspection.py": (
                "CurrentSourceAuthorization",
                "reconstruct_audit_for_access(",
            ),
            "document_artifact_experience.py": (
                "CurrentSourceAuthorization",
                "resolve_document_for_access(",
            ),
            "memory_knowledge_search_experience.py": (
                "CurrentSourceAuthorization",
                "freshness_state",
                "allowed_classifications",
            ),
            "operator_safety.py": (
                "CurrentSourceAuthorization",
                "_same_current_source_access(",
            ),
        }
        for module_name, tokens in reviewed.items():
            with self.subTest(module=module_name):
                source = (PLATFORM_ROOT / module_name).read_text(encoding="utf-8")
                self.assertNotIn("from .authority_safe_ux import", source)
                for token in tokens:
                    self.assertIn(token, source)

    def test_product_consequential_action_keeps_r10_and_governed_execution_choke_point(self) -> None:
        product_source = (PRODUCT_ROOT / "task_composition.py").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "from arvectum_os_ref.operator_safety import (", product_source
        )
        self.assertIn("prepare_operator_canonical_mutation_action(", product_source)
        self.assertIn("execute_operator_canonical_mutation_action(", product_source)
        self.assertNotIn(
            "from arvectum_os_ref.execution_action_experience import", product_source
        )

        platform_source = "\n".join(
            path.read_text(encoding="utf-8") for path in PLATFORM_ROOT.glob("*.py")
        )
        self.assertNotIn("bounded_product_ref", platform_source)
        self.assertNotIn("product.bounded-review-task", platform_source)
        self.assertNotIn("p4.08.record-task-decision", platform_source)


if __name__ == "__main__":
    unittest.main()
