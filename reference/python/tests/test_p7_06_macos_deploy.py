import pathlib
import subprocess
import unittest

HERE = pathlib.Path(__file__).resolve().parents[1]
DEPLOY = HERE / "p7_06_macos_deploy.sh"
PROOF = HERE / "p7_06_selected_mac_proof.sh"

class ShellTests(unittest.TestCase):
    def test_deploy_shell_syntax(self):
        subprocess.run(["sh", "-n", str(DEPLOY)], check=True)

    def test_proof_shell_syntax(self):
        subprocess.run(["sh", "-n", str(PROOF)], check=True)

    def test_no_network_client_or_remote_transport(self):
        text = DEPLOY.read_text()
        for token in ("curl ", "wget ", "ssh ", "scp ", "nc "):
            self.assertNotIn(token, text)

    def test_r22_and_governed_sequence_guards_present(self):
        text = DEPLOY.read_text()
        self.assertIn("R22_SHA=", text)
        self.assertLess(text.index('backup_preupdate "$source"'), text.index('sh "$P705" uninstall'))
        self.assertIn("compatibility/migration preflight rejected target", text)
        self.assertIn("rollback_and_record_failure", text)
        self.assertIn("restore_plist_and_start", text)

    def test_sibling_shell_adapters_do_not_require_executable_git_mode(self):
        text = DEPLOY.read_text()
        self.assertNotIn('\n  "$P702" ', text)
        self.assertNotIn('\n  "$P705" ', text)
        self.assertNotIn('if ! "$P702" ', text)
        self.assertNotIn('if ! "$P705" ', text)
        self.assertIn('sh "$P702" status', text)
        self.assertIn('sh "$P702" stop', text)
        self.assertIn('sh "$P702" install', text)
        self.assertIn('sh "$P705" status', text)
        self.assertIn('sh "$P705" uninstall', text)
        self.assertIn('sh "$P705" install', text)

    def test_first_r22_upgrade_admits_only_exact_proven_legacy_observer_shape(self):
        text = DEPLOY.read_text()
        self.assertIn(
            'P705_LEGACY_PROVEN_SHA="cf60e52c93bf0ef4158cf2c3e26792850a126c70"',
            text,
        )
        self.assertIn('verify_source_observer_preupdate "$source"', text)
        self.assertIn('rel" = "$P705_LEGACY_PROVEN_SHA', text)
        self.assertIn('payload.get("ProgramArguments") != expected', text)
        self.assertIn(
            "pre-R22 observer plist does not match the exact historically proven P7.05 shape",
            text,
        )
        self.assertIn("source observer legacy R22 carry-forward status PASS", text)

    def test_rollback_reinstalls_safe_exact_observer_instead_of_unsafe_legacy_plist(self):
        text = DEPLOY.read_text()
        self.assertNotIn('cp "$old_observer" "$OBSERVER_PLIST"', text)
        self.assertIn(
            'if ! sh "$P705" install >/dev/null; then fail "rollback observer exact-release re-pin failed"; fi',
            text,
        )
        self.assertIn(
            'if ! sh "$P705" status >/dev/null; then fail "rollback observer exact-release verification failed"; fi',
            text,
        )

    def test_selected_mac_proof_orders_update_rollback_reupdate(self):
        text = PROOF.read_text()
        self.assertLess(text.index('update "$DECISION_REF:update"'), text.index("rollback-last"))
        self.assertLess(text.index("rollback-last"), text.index('update "$DECISION_REF:final-update"'))
        self.assertIn("historical_effect_replay_invoked", text)
        self.assertIn("product_external_effect_invoked", text)

    def test_selected_mac_proof_does_not_require_executable_git_mode(self):
        text = PROOF.read_text()
        self.assertIn('sh "$DEPLOY" update "$DECISION_REF:update"', text)
        self.assertIn('sh "$DEPLOY" rollback-last', text)
        self.assertIn('sh "$DEPLOY" update "$DECISION_REF:final-update"', text)
        self.assertIn('sh "$DEPLOY" status', text)

    def test_selected_mac_proof_retains_digest_sidecar(self):
        text = PROOF.read_text()
        self.assertIn('> "$summary.sha256"', text)
        self.assertIn('chmod 600 "$summary.sha256"', text)

if __name__ == "__main__":
    unittest.main()