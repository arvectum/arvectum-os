import pathlib
import subprocess
import unittest

HERE = pathlib.Path(__file__).resolve().parents[1]
SERVICE = HERE / "p7_06_ui3_macos_operator.sh"


class UI3MacOSOperatorTests(unittest.TestCase):
    def test_shell_syntax(self):
        subprocess.run(["sh", "-n", str(SERVICE)], check=True)

    def test_listener_is_loopback_only_and_verified(self):
        text = SERVICE.read_text(encoding="utf-8")
        self.assertIn('HOST="127.0.0.1"', text)
        self.assertIn('lsof -nP -iTCP:"$port" -sTCP:LISTEN', text)
        self.assertIn('127.0.0.1:$port', text)
        self.assertNotIn('HOST="0.0.0.0"', text)

    def test_launchd_is_exact_release_pinned(self):
        text = SERVICE.read_text(encoding="utf-8")
        self.assertIn("release_python()", text)
        self.assertIn("release_script()", text)
        self.assertIn("verify_plist_release_pin", text)
        self.assertIn('if "/current/" in arg', text)
        self.assertNotIn('<string>$ROOT/current/', text)

    def test_no_remote_transport_or_secret_in_launchd_arguments(self):
        text = SERVICE.read_text(encoding="utf-8")
        for token in ("curl ", "wget ", "ssh ", "scp ", "nc "):
            self.assertNotIn(token, text)
        plist_start = text.index('cat > "$PLIST"')
        plist_end = text.index("EOF2", plist_start + 15)
        plist = text[plist_start:plist_end]
        self.assertNotIn("access.secret", plist)
        self.assertNotIn("show-access-secret", plist)

    def test_reversible_lifecycle_and_minimization_are_explicit(self):
        text = SERVICE.read_text(encoding="utf-8")
        self.assertIn("install_service()", text)
        self.assertIn("restart_service()", text)
        self.assertIn("uninstall_service()", text)
        self.assertIn("remove-private-material", text)
        self.assertIn("P7.04 grants/credentials unchanged", text)
        self.assertIn("process-local browser session invalidated", text)


if __name__ == "__main__":
    unittest.main()
