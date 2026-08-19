import pathlib
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import p7_06_ui3_selected_mac_proof_runner as runner


class UI3SelectedMacProofRunnerTests(unittest.TestCase):
    def test_detects_ui3_and_p706_deploy_shell_calls(self):
        self.assertTrue(runner._is_ui3_shell_call(("sh", "/tmp/p7_06_ui3_macos_operator.sh", "status")))
        self.assertFalse(runner._is_ui3_shell_call(("sh", "/tmp/p7_06_macos_deploy.sh", "update")))
        self.assertFalse(runner._is_ui3_shell_call(("python3", "/tmp/p7_06_ui3_macos_operator.sh", "status")))
        self.assertTrue(runner._is_p706_deploy_call(("sh", "/historical/p7_06_macos_deploy.sh", "update", "d")))
        self.assertTrue(runner._is_p706_deploy_call(("sh", "/historical/p7_06_macos_deploy.sh", "rollback-last")))
        self.assertFalse(runner._is_p706_deploy_call(("sh", "/historical/p7_06_macos_deploy.sh", "status")))

    def test_runner_source_enforces_exact_release_and_canonical_checkout(self):
        text = pathlib.Path(runner.__file__).read_text(encoding="utf-8")
        self.assertIn("supported proof runner must execute from the exact active release", text)
        self.assertIn("canonical checkout HEAD/origin-main must equal the exact active proof target", text)
        self.assertIn("target_controller", text)
        self.assertIn('value["historical_ui3_controller_replayed"] = False', text)
        self.assertIn('value["hardened_controller_runner_verified"] = True', text)
        self.assertIn('value["canonical_checkout_deploy_controller_verified"] = True', text)
        self.assertIn('value["release_snapshot_deploy_controller_invoked"] = False', text)
        self.assertIn('parser.add_argument("--repo-root", required=True)', text)

    def test_normal_ui3_call_uses_hardened_target_controller(self):
        calls = []

        def fake_original(*args):
            calls.append(args)

        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "runtime"
            repo = Path(td) / "repo"
            target = Path(td) / "target/p7_06_ui3_macos_operator.sh"
            runner._dispatch_core_run(
                fake_original,
                root,
                repo,
                target,
                ("sh", "/historical/p7_06_ui3_macos_operator.sh", "status"),
            )
        self.assertEqual(calls, [("sh", str(target), "status")])

    def test_governed_ui3_update_uses_canonical_governed_controller(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "runtime"
            repo = Path(td) / "repo"
            target = Path(td) / "target/p7_06_ui3_macos_operator.sh"
            with mock.patch.object(runner.governed, "governed_operation") as governed_call:
                runner._dispatch_core_run(
                    mock.Mock(),
                    root,
                    repo,
                    target,
                    ("sh", "/historical/p7_06_ui3_macos_operator.sh", "governed-update", "decision"),
                )
            governed_call.assert_called_once_with(root, repo, "update", "decision")

    def test_governed_ui3_rollback_uses_canonical_governed_controller(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "runtime"
            repo = Path(td) / "repo"
            target = Path(td) / "target/p7_06_ui3_macos_operator.sh"
            with mock.patch.object(runner.governed, "governed_operation") as governed_call:
                runner._dispatch_core_run(
                    mock.Mock(),
                    root,
                    repo,
                    target,
                    ("sh", "/historical/p7_06_ui3_macos_operator.sh", "governed-rollback-last"),
                )
            governed_call.assert_called_once_with(root, repo, "rollback-last")

    def test_direct_historical_deploy_call_is_routed_to_canonical_checkout(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "runtime"
            repo = Path(td) / "repo"
            target = Path(td) / "target/p7_06_ui3_macos_operator.sh"
            with mock.patch.object(runner.governed, "run_canonical_deploy") as deploy_call:
                runner._dispatch_core_run(
                    mock.Mock(),
                    root,
                    repo,
                    target,
                    ("sh", "/runtime/releases/source/p7_06_macos_deploy.sh", "update", "decision"),
                )
            deploy_call.assert_called_once_with(root, repo, ("update", "decision"))

    def test_core_remains_authoritative_for_p704_and_ui4_boundaries(self):
        core_text = pathlib.Path(runner.core.__file__).read_text(encoding="utf-8")
        self.assertNotIn("grant_access(", core_text)
        self.assertNotIn("issue_credential(", core_text)
        self.assertIn('"real_owner_interaction_invoked": False', core_text)
        self.assertIn('"organizational_authority_provided": False', core_text)


if __name__ == "__main__":
    unittest.main()
