import os
import subprocess
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
PYTHON_ROOT = HERE.parent
P702 = PYTHON_ROOT / "p7_02_macos_service.sh"


class P706CurrentReleasePointerTests(unittest.TestCase):
    def test_p702_shell_syntax_remains_valid(self):
        checked = subprocess.run(
            ["sh", "-n", str(P702)],
            cwd=str(PYTHON_ROOT),
            text=True,
            capture_output=True,
            timeout=5,
        )
        self.assertEqual(checked.returncode, 0, checked.stderr)

    def test_install_does_not_use_mv_into_directory_symlink_for_current_pointer(self):
        text = P702.read_text(encoding="utf-8")
        self.assertNotIn(
            'mv -f "$RUNTIME_ROOT/current.new" "$RUNTIME_ROOT/current"',
            text,
        )
        self.assertIn("os.replace(source, destination)", text)

    def test_replacement_fails_closed_if_current_is_not_a_symlink(self):
        text = P702.read_text(encoding="utf-8")
        self.assertIn("os.lstat(destination).st_mode", text)
        self.assertIn("stat.S_ISLNK(mode)", text)
        self.assertIn("current release pointer exists and is not a symbolic link", text)

    def test_install_verifies_exact_pointer_before_plist_and_activation(self):
        text = P702.read_text(encoding="utf-8")
        install = text.index("install_runtime() {")
        replace = text.index("replace_current_release", install)
        verify = text.index('[ "$(current_release)" = "$HEAD_SHA" ]', replace)
        plist = text.index('write_plist "$HEAD_SHA"', verify)
        bootstrap = text.index('launchctl bootstrap "$DOMAIN" "$LAUNCH_AGENT"', plist)
        self.assertLess(replace, verify)
        self.assertLess(verify, plist)
        self.assertLess(plist, bootstrap)

    def test_os_replace_replaces_symlink_itself_instead_of_following_directory_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old_release = root / "old"
            new_release = root / "new"
            old_release.mkdir()
            new_release.mkdir()
            current = root / "current"
            prepared = root / "current.new"
            current.symlink_to(old_release, target_is_directory=True)
            prepared.symlink_to(new_release, target_is_directory=True)

            os.replace(prepared, current)

            self.assertTrue(current.is_symlink())
            self.assertEqual(Path(os.readlink(current)), new_release)
            self.assertFalse(prepared.exists())
            self.assertEqual(list(old_release.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
