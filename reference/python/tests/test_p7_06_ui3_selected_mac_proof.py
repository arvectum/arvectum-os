import pathlib
import unittest

PROOF = pathlib.Path(__file__).resolve().parents[1] / "p7_06_ui3_selected_mac_proof.py"


class UI3SelectedMacProofSourceTests(unittest.TestCase):
    def setUp(self):
        self.text = PROOF.read_text(encoding="utf-8")

    def test_requires_exact_active_release_and_python(self):
        self.assertIn("proof runner must execute from the exact active release", self.text)
        self.assertIn("proof runner must use the exact active-release Python", self.text)
        self.assertIn("p7-06-last-success.json", self.text)
        self.assertIn("active release is not the target of the last governed P7.06 update", self.text)

    def test_never_provisions_p704_access(self):
        self.assertNotIn("grant_access(", self.text)
        self.assertNotIn("issue_credential(", self.text)
        self.assertIn('"p704_grants_or_credentials_created_by_ui3": False', self.text)
        self.assertIn("_p704_digest", self.text)

    def test_http_proof_covers_unlock_and_restart_session_invalidation(self):
        self.assertIn("if status != 401", self.text)
        self.assertIn("if status != 303", self.text)
        self.assertIn("definitely-wrong-ui3-secret", self.text)
        self.assertIn("HttpOnly", self.text)
        self.assertIn("SameSite=Strict", self.text)
        self.assertIn('_run("sh", str(ui3_shell), "restart")', self.text)
        self.assertIn("restart did not invalidate prior browser session", self.text)
        self.assertIn("ingress secret leaked", self.text)

    def test_lifecycle_and_rollback_are_reversible(self):
        self.assertIn('_run("sh", str(ui3_shell), "uninstall")', self.text)
        self.assertIn('_run("sh", str(ui3_shell), "install")', self.text)
        self.assertIn('_run("sh", str(ui3_shell), "governed-rollback-last")', self.text)
        self.assertIn('_run("sh", str(source_ui3), "governed-update",', self.text)
        self.assertIn('_run("sh", str(source_deploy), "update",', self.text)
        self.assertIn("rollback to pre-UI3 source did not remove UI3 private surface", self.text)
        self.assertIn("final governed update did not restore the exact proof target", self.text)
        self.assertIn('Path.home() / "Library" / "LaunchAgents"', self.text)

    def test_proof_guards_canonical_and_access_state(self):
        self.assertIn("_canonical_digest(root)", self.text)
        self.assertIn("_p704_digest(root)", self.text)
        self.assertIn('"p704_state_unchanged": True', self.text)
        self.assertIn('"p703_governed_checkpoint_state_unchanged": True', self.text)
        self.assertIn('"canonical_mutation_performed_by_ui3": False', self.text)
        self.assertIn('"product_external_effect_invoked": False', self.text)

    def test_ui4_real_interaction_remains_out_of_scope(self):
        self.assertIn('"interaction_provider": "none-until-p7-06-ui4"', self.text)
        self.assertIn('"real_owner_interaction_invoked": False', self.text)
        self.assertIn('"organizational_authority_provided": False', self.text)
        self.assertIn('"consequential_approval_provided": False', self.text)


if __name__ == "__main__":
    unittest.main()
