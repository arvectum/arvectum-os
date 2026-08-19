import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import p7_06_ui3_canonical_governed_controller as c


SHA_A = "a" * 40


class CanonicalGovernedControllerTests(unittest.TestCase):
    def test_validate_sha(self):
        self.assertEqual(c._validate_sha(SHA_A, "x"), SHA_A)
        with self.assertRaises(c.UI3GovernedControllerError):
            c._validate_sha("short", "x")

    def test_canonical_head_requires_exact_origin_and_synced_main(self):
        good = [
            mock.Mock(returncode=0, stdout="main\n", stderr=""),
            mock.Mock(returncode=0, stdout="", stderr=""),
            mock.Mock(returncode=0, stdout="https://github.com/arvectum/arvectum-os.git\n", stderr=""),
            mock.Mock(returncode=0, stdout="", stderr=""),
            mock.Mock(returncode=0, stdout=SHA_A + "\n", stderr=""),
            mock.Mock(returncode=0, stdout=SHA_A + "\n", stderr=""),
        ]
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            (repo / ".git").mkdir()
            with mock.patch.object(c, "_run", side_effect=good):
                self.assertEqual(c.canonical_head(repo), SHA_A)

            bad = [
                mock.Mock(returncode=0, stdout="main\n", stderr=""),
                mock.Mock(returncode=0, stdout="", stderr=""),
                mock.Mock(returncode=0, stdout="https://github.com/arvectum/arvectum-os-evil.git\n", stderr=""),
            ]
            with mock.patch.object(c, "_run", side_effect=bad):
                with self.assertRaises(c.UI3GovernedControllerError):
                    c.canonical_head(repo)

    def test_current_release_reads_exact_symlink(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            target = root / "releases" / SHA_A
            target.mkdir(parents=True)
            (root / "current").symlink_to(target)
            self.assertEqual(c.current_release(root), SHA_A)

    def test_current_has_ui3_requires_exact_current_module(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base = root / "releases" / SHA_A / "source/reference/python"
            base.mkdir(parents=True)
            (root / "current").symlink_to(root / "releases" / SHA_A)
            self.assertFalse(c._current_has_ui3(root))
            (base / "p7_06_ui3_private_operator.py").write_text("", encoding="utf-8")
            self.assertTrue(c._current_has_ui3(root))

    def test_canonical_deploy_uses_checkout_controller_not_release_snapshot(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "runtime"
            repo = Path(td) / "repo"
            root.mkdir()
            deploy = repo / "reference/python/p7_06_macos_deploy.sh"
            ui3 = repo / "reference/python/p7_06_ui3_macos_operator.sh"
            deploy.parent.mkdir(parents=True)
            deploy.write_text("", encoding="utf-8")
            ui3.write_text("", encoding="utf-8")
            result = mock.Mock(returncode=0, stdout="", stderr="")
            with (
                mock.patch.object(c, "canonical_head", return_value=SHA_A),
                mock.patch.object(c, "_run", return_value=result) as run_mock,
            ):
                c.run_canonical_deploy(root, repo, ["update", "decision"])
            command = run_mock.call_args.args[0]
            self.assertEqual(command[0], "sh")
            self.assertEqual(Path(command[1]), deploy)
            self.assertNotIn("/releases/", command[1])

    def test_governed_operation_stops_deploys_and_reconciles(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "runtime"
            repo = Path(td) / "repo"
            root.mkdir()
            repo.mkdir()
            calls = []
            with (
                mock.patch.object(c, "canonical_head", return_value=SHA_A),
                mock.patch.object(c, "_controller_paths", return_value=(Path("ui3"), Path("deploy"))),
                mock.patch.object(c, "_service_loaded", return_value=True),
                mock.patch.object(c, "_run_ui3", side_effect=lambda _r, _root, *args, **_kw: calls.append(("ui3", args))),
                mock.patch.object(c, "run_canonical_deploy", side_effect=lambda _root, _repo, args: calls.append(("deploy", tuple(args)))),
                mock.patch.object(c, "reconcile_current", side_effect=lambda _root, _repo: calls.append(("reconcile", ()))),
            ):
                c.governed_operation(root, repo, "rollback-last")
            self.assertEqual(
                calls,
                [
                    ("ui3", ("status",)),
                    ("ui3", ("stop",)),
                    ("deploy", ("rollback-last",)),
                    ("reconcile", ()),
                ],
            )

    def test_failed_deploy_still_reconciles_before_failure(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "runtime"
            repo = Path(td) / "repo"
            root.mkdir()
            repo.mkdir()
            reconciled = []
            with (
                mock.patch.object(c, "canonical_head", return_value=SHA_A),
                mock.patch.object(c, "_controller_paths", return_value=(Path("ui3"), Path("deploy"))),
                mock.patch.object(c, "_service_loaded", return_value=False),
                mock.patch.object(c, "run_canonical_deploy", side_effect=c.UI3GovernedControllerError("forced")),
                mock.patch.object(c, "reconcile_current", side_effect=lambda _root, _repo: reconciled.append(True)),
            ):
                with self.assertRaises(c.UI3GovernedControllerError):
                    c.governed_operation(root, repo, "update", "decision")
            self.assertEqual(reconciled, [True])

    def test_private_cleanup_scope_excludes_p704(self):
        names = {str(path) for path in c._known_private_paths(Path("/runtime"))}
        self.assertTrue(any("p7-06-ui3" in name for name in names))
        self.assertFalse(any("p7-04" in name for name in names))
        source = Path(c.__file__).read_text(encoding="utf-8")
        self.assertNotIn('releases/%s/source/reference/python/p7_06_macos_deploy.sh', source)
        self.assertIn("run_canonical_deploy", source)


if __name__ == "__main__":
    unittest.main()
