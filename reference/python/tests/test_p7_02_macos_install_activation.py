import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SERVICE = HERE.parent / "p7_02_macos_service.sh"


def block(text: str, start_name: str, end_name: str) -> str:
    start = text.index(f"{start_name}()")
    end = text.index(f"{end_name}()", start)
    return text[start:end]


class P702MacosInstallActivationTests(unittest.TestCase):
    def test_install_uses_runatload_bootstrap_without_forced_replacement(self):
        text = SERVICE.read_text(encoding="utf-8")
        install = block(text, "install_runtime", "start_runtime")
        bootstrap = install.index('launchctl bootstrap "$DOMAIN" "$LAUNCH_AGENT"')
        healthy = install.index('wait_healthy || fail "runtime did not become healthy after install"')
        self.assertLess(bootstrap, healthy)
        self.assertNotIn('kickstart -k "$SERVICE_TARGET"', install)

    def test_plist_declares_runatload_and_explicit_restart_still_forces_replacement(self):
        text = SERVICE.read_text(encoding="utf-8")
        self.assertIn('"RunAtLoad": True', text)
        restart = block(text, "restart_runtime", "status_runtime")
        self.assertIn('launchctl kickstart -k "$SERVICE_TARGET"', restart)


if __name__ == "__main__":
    unittest.main()
