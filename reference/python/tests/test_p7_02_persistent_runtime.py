import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
PYTHON_ROOT = HERE.parent
RUNTIME_SCRIPT = PYTHON_ROOT / "p7_02_persistent_runtime.py"
SERVICE_SCRIPT = PYTHON_ROOT / "p7_02_macos_service.sh"
RELEASE_SHA = "a" * 40


class P702PersistentRuntimeTests(unittest.TestCase):
    def _start(self, root: Path) -> subprocess.Popen[str]:
        return subprocess.Popen(
            [
                sys.executable,
                str(RUNTIME_SCRIPT),
                "run",
                "--runtime-root",
                str(root),
                "--release-sha",
                RELEASE_SHA,
                "--heartbeat-seconds",
                "0.05",
            ],
            cwd=str(PYTHON_ROOT),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def _wait_health(self, root: Path, expected_generation=None, timeout=5.0):
        health_path = root / "run" / "health.json"
        deadline = time.time() + timeout
        last = None
        while time.time() < deadline:
            try:
                last = json.loads(health_path.read_text(encoding="utf-8"))
            except (FileNotFoundError, json.JSONDecodeError):
                time.sleep(0.02)
                continue
            if last.get("state") == "healthy" and (
                expected_generation is None or last.get("generation") == expected_generation
            ):
                return last
            time.sleep(0.02)
        self.fail(f"health did not become ready; last={last!r}")

    def _terminate(self, proc: subprocess.Popen[str]):
        try:
            if proc.poll() is None:
                proc.terminate()
                proc.wait(timeout=5)
        finally:
            if proc.stdout is not None:
                proc.stdout.close()
            if proc.stderr is not None:
                proc.stderr.close()

    def _fake_macos_launchctl_env(self, root: Path, *, state: str, delay_polls: int, attempts: int):
        fake_bin = root / "fake-bin"
        fake_bin.mkdir()
        state_file = root / "launchctl-state"
        state_file.write_text(state, encoding="utf-8")

        uname = fake_bin / "uname"
        uname.write_text("#!/bin/sh\nprintf 'Darwin\\n'\n", encoding="utf-8")
        uname.chmod(0o755)

        launchctl = fake_bin / "launchctl"
        launchctl.write_text(
            """#!/bin/sh
set -eu
STATE_FILE=${P7_FAKE_LAUNCHCTL_STATE:?}
DELAY_POLLS=${P7_FAKE_BOOTOUT_DELAY_POLLS:-0}
cmd=${1:-}
case "$cmd" in
  print)
    [ -f "$STATE_FILE" ] || exit 1
    state=$(cat "$STATE_FILE")
    case "$state" in
      loaded)
        exit 0
        ;;
      unloading:*)
        remaining=${state#unloading:}
        if [ "$remaining" -gt 0 ]; then
          printf 'unloading:%s\\n' "$((remaining - 1))" > "$STATE_FILE"
          exit 0
        fi
        printf 'unloaded\\n' > "$STATE_FILE"
        exit 1
        ;;
      *)
        exit 1
        ;;
    esac
    ;;
  bootout)
    printf 'unloading:%s\\n' "$DELAY_POLLS" > "$STATE_FILE"
    exit 0
    ;;
  *)
    exit 0
    ;;
esac
""",
            encoding="utf-8",
        )
        launchctl.chmod(0o755)

        env = os.environ.copy()
        env["HOME"] = str(root / "home")
        env["PATH"] = f"{fake_bin}{os.pathsep}{env.get('PATH', '')}"
        env["P7_FAKE_LAUNCHCTL_STATE"] = str(state_file)
        env["P7_FAKE_BOOTOUT_DELAY_POLLS"] = str(delay_polls)
        env["ARVECTUM_P7_02_SERVICE_WAIT_ATTEMPTS"] = str(attempts)
        env["ARVECTUM_P7_02_SERVICE_WAIT_INTERVAL"] = "0"
        return env, state_file

    def test_runtime_health_is_local_noncanonical_and_effect_free(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            proc = self._start(root)
            try:
                health = self._wait_health(root, expected_generation=1)
                self.assertEqual(health["schema"], "arvectum.p7_02.runtime-health/1")
                self.assertEqual(health["classification"], "non-canonical operational telemetry")
                self.assertEqual(health["operating_mode"], "Persistent Internal / owner-operated")
                self.assertEqual(health["organization_scope"], "ООО «Арвектум»")
                self.assertEqual(health["network_listener_mode"], "none")
                self.assertFalse(health["product_effects_enabled"])
                self.assertFalse(health["canonical_state_written"])
                self.assertTrue(health["semantic_imports_ok"])
                self.assertEqual(health["release_sha"], RELEASE_SHA)
                self.assertEqual(health["pid"], proc.pid)
                self.assertEqual(os.stat(root / "run" / "health.json").st_mode & 0o777, 0o600)

                checked = subprocess.run(
                    [
                        sys.executable,
                        str(RUNTIME_SCRIPT),
                        "check",
                        "--runtime-root",
                        str(root),
                        "--expected-release",
                        RELEASE_SHA,
                        "--max-age-seconds",
                        "2",
                    ],
                    cwd=str(PYTHON_ROOT),
                    text=True,
                    capture_output=True,
                    timeout=5,
                )
                self.assertEqual(checked.returncode, 0, checked.stderr)
                self.assertIn("P7.02 health PASS", checked.stdout)
            finally:
                self._terminate(proc)

    def test_single_instance_lock_and_generation_after_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = self._start(root)
            try:
                first_health = self._wait_health(root, expected_generation=1)
                second = self._start(root)
                second_out, second_err = second.communicate(timeout=5)
                self.assertEqual(second.returncode, 73, second_out + second_err)
                self.assertIn("already has an active owner process", second_err)
            finally:
                self._terminate(first)

            stopped = json.loads((root / "run" / "health.json").read_text(encoding="utf-8"))
            self.assertEqual(stopped["state"], "stopped")

            replacement = self._start(root)
            try:
                replacement_health = self._wait_health(root, expected_generation=2)
                self.assertEqual(replacement_health["previous_instance_id"], first_health["instance_id"])
                self.assertNotEqual(replacement_health["instance_id"], first_health["instance_id"])
            finally:
                self._terminate(replacement)

    def test_stale_or_stopped_health_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            proc = self._start(root)
            try:
                self._wait_health(root)
            finally:
                self._terminate(proc)

            checked = subprocess.run(
                [
                    sys.executable,
                    str(RUNTIME_SCRIPT),
                    "check",
                    "--runtime-root",
                    str(root),
                    "--expected-release",
                    RELEASE_SHA,
                    "--max-age-seconds",
                    "2",
                ],
                cwd=str(PYTHON_ROOT),
                text=True,
                capture_output=True,
                timeout=5,
            )
            self.assertNotEqual(checked.returncode, 0)
            self.assertIn("state='stopped'", checked.stderr)

    def test_release_pin_requires_full_commit_sha(self):
        with tempfile.TemporaryDirectory() as tmp:
            checked = subprocess.run(
                [
                    sys.executable,
                    str(RUNTIME_SCRIPT),
                    "run",
                    "--runtime-root",
                    tmp,
                    "--release-sha",
                    "abc123",
                    "--heartbeat-seconds",
                    "0.05",
                ],
                cwd=str(PYTHON_ROOT),
                text=True,
                capture_output=True,
                timeout=5,
            )
            self.assertNotEqual(checked.returncode, 0)
            self.assertIn("release SHA must be a full 40-character Git commit SHA", checked.stderr)
            self.assertFalse((Path(tmp) / "run" / "health.json").exists())

    def test_macos_lifecycle_adapter_has_valid_posix_shell_syntax(self):
        checked = subprocess.run(
            ["sh", "-n", str(SERVICE_SCRIPT)],
            cwd=str(PYTHON_ROOT),
            text=True,
            capture_output=True,
            timeout=5,
        )
        self.assertEqual(checked.returncode, 0, checked.stderr)

    def test_stop_waits_for_asynchronous_launchd_bootout(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            env, state_file = self._fake_macos_launchctl_env(
                root,
                state="loaded\n",
                delay_polls=2,
                attempts=5,
            )
            checked = subprocess.run(
                ["sh", str(SERVICE_SCRIPT), "stop"],
                cwd=str(PYTHON_ROOT),
                env=env,
                text=True,
                capture_output=True,
                timeout=5,
            )
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertIn("P7.02: stop PASS", checked.stdout)
            self.assertEqual(state_file.read_text(encoding="utf-8").strip(), "unloaded")

    def test_stop_fails_closed_when_launchd_never_finishes_unload(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            env, state_file = self._fake_macos_launchctl_env(
                root,
                state="loaded\n",
                delay_polls=50,
                attempts=3,
            )
            checked = subprocess.run(
                ["sh", str(SERVICE_SCRIPT), "stop"],
                cwd=str(PYTHON_ROOT),
                env=env,
                text=True,
                capture_output=True,
                timeout=5,
            )
            self.assertNotEqual(checked.returncode, 0)
            self.assertIn("service remains loaded after bounded stop wait", checked.stderr)
            self.assertTrue(state_file.read_text(encoding="utf-8").startswith("unloading:"))

    def test_stop_is_idempotent_when_launchd_target_is_already_unloaded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            env, state_file = self._fake_macos_launchctl_env(
                root,
                state="unloaded\n",
                delay_polls=0,
                attempts=3,
            )
            checked = subprocess.run(
                ["sh", str(SERVICE_SCRIPT), "stop"],
                cwd=str(PYTHON_ROOT),
                env=env,
                text=True,
                capture_output=True,
                timeout=5,
            )
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertIn("P7.02: stop PASS", checked.stdout)
            self.assertEqual(state_file.read_text(encoding="utf-8").strip(), "unloaded")

    def test_runtime_source_does_not_create_a_network_service(self):
        source = RUNTIME_SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("import socket", source)
        self.assertNotIn("from socket", source)
        self.assertNotIn("http.server", source)
        self.assertNotIn("serve_forever", source)


if __name__ == "__main__":
    unittest.main()
