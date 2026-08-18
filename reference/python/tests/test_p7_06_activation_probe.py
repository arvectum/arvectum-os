import subprocess
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
PYTHON_ROOT = HERE.parent
PROBE = PYTHON_ROOT / "p7_06_activation_probe.sh"

class P706ActivationProbeTests(unittest.TestCase):
    def test_probe_has_valid_posix_shell_syntax(self):
        checked = subprocess.run(["sh", "-n", str(PROBE)], cwd=str(PYTHON_ROOT), text=True, capture_output=True, timeout=5)
        self.assertEqual(checked.returncode, 0, checked.stderr)

    def test_probe_delegates_lifecycle_to_governed_p706_adapter(self):
        text = PROBE.read_text(encoding="utf-8")
        self.assertIn('sh "$DEPLOY" update "$DECISION_REF"', text)
        self.assertIn('sh "$DEPLOY" rollback-last', text)
        self.assertIn('sh "$DEPLOY" status', text)
        self.assertNotIn("launchctl bootstrap", text)
        self.assertNotIn("launchctl bootout", text)
        self.assertNotIn("launchctl kickstart", text)

    def test_probe_scopes_process_diagnostics_to_runtime_lock_owners(self):
        text = PROBE.read_text(encoding="utf-8")
        self.assertIn('lsof -t "$LOCK_FILE"', text)
        self.assertIn('ps -p "$pid" -o pid=,ppid=,command=', text)
        self.assertNotIn("ps -ax", text)
        self.assertNotIn("ps aux", text)

    def test_probe_is_effect_free_except_existing_update_rollback_lifecycle(self):
        text = PROBE.read_text(encoding="utf-8")
        for forbidden in ("curl ", "wget ", "ssh ", "scp ", "nc "):
            self.assertNotIn(forbidden, text)
        self.assertIn('"canonical_mutation_performed_by_probe": False', text)
        self.assertIn('"product_external_effect_invoked": False', text)
        self.assertIn('"historical_effect_replay_invoked": False', text)

    def test_successful_diagnostic_update_is_rolled_back(self):
        text = PROBE.read_text(encoding="utf-8")
        update = text.index('if [ "$UPDATE_RC" -eq 0 ]; then')
        rollback = text.index('sh "$DEPLOY" rollback-last', update)
        final_status = text.index('sh "$DEPLOY" status', rollback)
        self.assertLess(update, rollback)
        self.assertLess(rollback, final_status)

if __name__ == "__main__":
    unittest.main()
