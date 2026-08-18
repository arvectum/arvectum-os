import shutil
import subprocess
import unittest
from pathlib import Path


class P705MacOSObserverAdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = Path(__file__).resolve().parents[1] / "p7_05_macos_observer.sh"
        cls.source = cls.script.read_text(encoding="utf-8")

    def test_observer_adapter_has_valid_posix_shell_syntax(self):
        shell = shutil.which("sh")
        if shell is None:
            self.skipTest("POSIX sh unavailable")
        result = subprocess.run(
            [shell, "-n", str(self.script)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_observer_is_periodic_local_adapter_without_network_client(self):
        self.assertIn("StartInterval", self.source)
        self.assertIn("p7_05_operational_visibility.py", self.source)
        self.assertIn("observe", self.source)
        for forbidden in ("http://", "https://", "curl ", "wget ", "nc ", "socat "):
            self.assertNotIn(forbidden, self.source)

    def test_observer_execution_is_pinned_to_one_exact_release(self):
        self.assertIn('release_observer()', self.source)
        self.assertIn('/releases/%s/source/reference/python/p7_05_operational_visibility.py', self.source)
        self.assertNotIn('/current/source/reference/python/p7_05_operational_visibility.py', self.source)
        self.assertIn('observer release pin mismatch', self.source)
        self.assertIn('/current/', self.source)
        self.assertIn('observer script must be pinned to an exact release, not current/', self.source)

    def test_observer_lifecycle_fails_closed_on_unloaded_or_async_bootout(self):
        self.assertIn('wait_unloaded()', self.source)
        self.assertIn('unload_observer()', self.source)
        self.assertIn('existing observer did not unload within bounded wait', self.source)
        self.assertIn('observer remains loaded after bounded uninstall wait', self.source)
        self.assertIn('launchd observer is not loaded', self.source)
        self.assertNotIn('launchctl bootout "$TARGET" >/dev/null 2>&1 || true', self.source)


if __name__ == "__main__":
    unittest.main()
