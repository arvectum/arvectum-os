import pathlib
import subprocess
import unittest

HERE = pathlib.Path(__file__).resolve().parents[1]
SERVICE = HERE / "p7_06_ui3_macos_operator.sh"


class UI3MacOSOperatorTests(unittest.TestCase):
    def test_shell_syntax(self):
        subprocess.run(["sh", "-n", str(SERVICE)], check=True)

    def test_listener_is_loopback_only_and_bound_to_launchd_pid(self):
        text = SERVICE.read_text(encoding="utf-8")
        self.assertIn('HOST="127.0.0.1"', text)
        self.assertIn("service_pid()", text)
        self.assertIn('lsof -nP -a -p "$pid" -iTCP:"$port" -sTCP:LISTEN', text)
        self.assertIn('another process/listener shares the UI3 private port', text)
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
        self.assertIn("cleanup_ui3_material()", text)
        self.assertIn("p7-06-ui3.stdout.log", text)
        self.assertIn("P7.04 grants/credentials unchanged", text)
        self.assertIn("process-local browser session invalidated", text)
        self.assertIn("wait_listener_ready", text)

    def test_launchd_waits_for_listener_readiness_not_only_pid(self):
        text = SERVICE.read_text(encoding="utf-8")
        self.assertIn("listener_matches()", text)
        self.assertIn("wait_listener_ready()", text)
        self.assertIn("sleep 0.25", text)
        install_start = text.index("install_service()")
        status_start = text.index("status_service()", install_start)
        install = text[install_start:status_start]
        self.assertLess(install.index("stop_service"), install.index('assert_port_free "$port"'))
        self.assertLess(
            install.index('assert_port_free "$port"'),
            install.index('launchctl bootstrap "$DOMAIN" "$PLIST"'),
        )
        self.assertLess(
            install.index('launchctl kickstart -k "$TARGET"'),
            install.index('wait_listener_ready "$port"'),
        )
        self.assertLess(install.index('wait_listener_ready "$port"'), install.index("status_service"))

    def test_port_collision_fails_explicitly_before_launchd_start(self):
        text = SERVICE.read_text(encoding="utf-8")
        self.assertIn("assert_port_free()", text)
        self.assertIn("is already in use before launchd start", text)
        self.assertIn("is owned by another listener", text)

    def test_restart_and_secret_rotation_wait_for_listener_readiness(self):
        text = SERVICE.read_text(encoding="utf-8")
        restart_start = text.index("restart_service()")
        show_start = text.index("show_secret()", restart_start)
        restart = text[restart_start:show_start]
        self.assertIn('wait_listener_ready "$port"', restart)
        rotate_start = text.index("rotate_secret()")
        reconcile_start = text.index("reconcile_after_deploy()", rotate_start)
        rotate = text[rotate_start:reconcile_start]
        self.assertIn('wait_listener_ready "$port"', rotate)

    def test_status_verifies_private_material_modes_and_secret_log_minimization(self):
        text = SERVICE.read_text(encoding="utf-8")
        self.assertIn("verify_private_material()", text)
        self.assertIn("path.stat().st_mode & 0o077", text)
        self.assertIn("plist.read_bytes() != service_copy.read_bytes()", text)
        self.assertIn("secret_bytes in stdout_log.read_bytes()", text)
        self.assertIn("secret_bytes in stderr_log.read_bytes()", text)
        status_start = text.index("status_service()")
        restart_start = text.index("restart_service()", status_start)
        status = text[status_start:restart_start]
        self.assertIn('verify_private_material "$rel"', status)

    def test_governed_deploy_wrapper_quiesces_and_reconciles_ui3(self):
        text = SERVICE.read_text(encoding="utf-8")
        update_start = text.index("governed_update()")
        rollback_start = text.index("governed_rollback()", update_start)
        update = text[update_start:rollback_start]
        self.assertLess(update.index("stop_service"), update.index('sh "$deploy" update "$1"'))
        self.assertLess(update.index('sh "$deploy" update "$1"'), update.index("reconcile_after_deploy"))
        rollback_end = text.index("uninstall_service()", rollback_start)
        rollback = text[rollback_start:rollback_end]
        self.assertLess(rollback.index("stop_service"), rollback.index('sh "$deploy" rollback-last'))
        self.assertLess(rollback.index('sh "$deploy" rollback-last'), rollback.index("reconcile_after_deploy"))
        self.assertIn('sh "$next" install', text)
        self.assertIn("UI3=absent-in-release", text)
        self.assertIn("use governed-update/governed-rollback-last", text)


if __name__ == "__main__":
    unittest.main()
