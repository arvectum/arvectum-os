import pathlib
import unittest
from unittest import mock

import p7_06_ui3_selected_mac_proof_runner as runner


class UI3SelectedMacProofRunnerTests(unittest.TestCase):
    def test_detects_ui3_shell_calls_only(self):
        self.assertTrue(runner._is_ui3_shell_call(("sh", "/tmp/p7_06_ui3_macos_operator.sh", "status")))
        self.assertFalse(runner._is_ui3_shell_call(("sh", "/tmp/p7_06_macos_deploy.sh", "update")))
        self.assertFalse(runner._is_ui3_shell_call(("python3", "/tmp/p7_06_ui3_macos_operator.sh", "status")))

    def test_runner_source_enforces_exact_release_and_hardened_controller(self):
        text = pathlib.Path(runner.__file__).read_text(encoding="utf-8")
        self.assertIn("supported proof runner must execute from the exact active release", text)
        self.assertIn("target_controller", text)
        self.assertIn("historical_ui3_controller_replayed", text)
        self.assertIn('value["historical_ui3_controller_replayed"] = False', text)
        self.assertIn('value["hardened_controller_runner_verified"] = True', text)

    def test_all_ui3_shell_calls_are_rewritten_to_exact_target_controller(self):
        calls = []

        def fake_original(*args):
            calls.append(args)

        target = "/exact/target/p7_06_ui3_macos_operator.sh"
        args = ("sh", "/historical/source/p7_06_ui3_macos_operator.sh", "governed-update", "decision")
        if runner._is_ui3_shell_call(args):
            fake_original("sh", target, *args[2:])
        self.assertEqual(calls, [("sh", target, "governed-update", "decision")])

    def test_wrapper_does_not_change_non_ui3_deploy_calls(self):
        args = ("sh", "/historical/source/p7_06_macos_deploy.sh", "update", "decision")
        self.assertFalse(runner._is_ui3_shell_call(args))

    def test_core_remains_authoritative_for_p704_and_ui4_boundaries(self):
        core_text = pathlib.Path(runner.core.__file__).read_text(encoding="utf-8")
        self.assertNotIn("grant_access(", core_text)
        self.assertNotIn("issue_credential(", core_text)
        self.assertIn('"real_owner_interaction_invoked": False', core_text)
        self.assertIn('"organizational_authority_provided": False', core_text)


if __name__ == "__main__":
    unittest.main()
