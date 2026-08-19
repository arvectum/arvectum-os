import json
import os
import pathlib
import stat
import tempfile
import unittest

from arvectum_os_ref.identity import Identity
import p7_04_persistent_access as p704
import p7_06_ui1_live_workspace as ui1
import p7_06_ui2_governed_interaction as ui2
import p7_06_ui3_private_operator as ui3
import p7_06_ui4_owner_preflight as ui4


class UI3PrivateOperatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name) / "runtime"
        self.org = Identity("organization", "arvectum-test", "platform")
        self.human = Identity("principal", "owner-human", self.org.value)
        p704.initialize_access_store(self.root, self.org)
        p704.register_principal(self.root, self.human, kind="human")
        issued = p704.issue_credential(self.root, self.human)
        self.credential_id = issued["credential_id"]

    def tearDown(self):
        self.tmp.cleanup()

    def _grant_ui1_ui2(self):
        inspect = p704.grant_access(
            self.root,
            self.human,
            operation=ui1.WORKSPACE_OPERATION,
            resource=ui1.WORKSPACE_RESOURCE,
            access_paths=("local",),
        )
        interact = p704.grant_access(
            self.root,
            self.human,
            operation=ui2.INTERACTION_OPERATION,
            resource=ui2.INTERACTION_RESOURCE,
            access_paths=("local",),
        )
        return inspect, interact

    def test_denied_grant_preflight_leaves_no_ui3_private_material(self):
        with self.assertRaises(ui3.UI3AccessDenied):
            ui3.resolve_operator_access(self.root, self.credential_id)
        self.assertFalse((self.root / "config" / "p7-06-ui3.json").exists())
        self.assertFalse((self.root / "secrets" / "p7-06-ui3" / "access.secret").exists())

    def test_exact_human_grant_set_resolves_without_authority(self):
        inspect, interact = self._grant_ui1_ui2()
        access = ui3.resolve_operator_access(self.root, self.credential_id)
        self.assertEqual(access.credential_id, self.credential_id)
        self.assertEqual(access.inspect_grant_id, inspect)
        self.assertEqual(access.interaction_grant_id, interact)
        self.assertEqual(access.principal, self.human)
        self.assertEqual(access.organization, self.org)

    def test_config_and_ingress_secret_are_owner_only_and_separate(self):
        self._grant_ui1_ui2()
        access = ui3.resolve_operator_access(self.root, self.credential_id)
        result = ui3.initialize_private_access(
            self.root, credential_id=access.credential_id, host="127.0.0.1", port=8765
        )
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["ui4_preflight_enabled"])
        config_path = self.root / "config" / "p7-06-ui3.json"
        secret_path = self.root / "secrets" / "p7-06-ui3" / "access.secret"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertEqual(config["listener_scope"], "ipv4-loopback-only")
        self.assertEqual(config["listener_host"], "127.0.0.1")
        self.assertEqual(config["interaction_provider"], ui3.UI4_PROVIDER)
        self.assertFalse(config["organizational_authority_provided"])
        self.assertFalse(config["consequential_approval_provided"])
        self.assertFalse(config["canonical_mutation_performed"])
        if os.name != "nt":
            self.assertEqual(stat.S_IMODE(config_path.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(secret_path.stat().st_mode), 0o600)
        secret = secret_path.read_text(encoding="utf-8").strip()
        self.assertGreater(len(secret), 32)
        self.assertNotIn(secret, config_path.read_text(encoding="utf-8"))

    def test_legacy_ui3_config_migrates_provider_without_rotating_secret_or_p704(self):
        self._grant_ui1_ui2()
        access = ui3.resolve_operator_access(self.root, self.credential_id)
        ui3.initialize_private_access(self.root, credential_id=access.credential_id)
        config_path = self.root / "config" / "p7-06-ui3.json"
        secret_path = self.root / "secrets" / "p7-06-ui3" / "access.secret"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        config["interaction_provider"] = ui3.LEGACY_PROVIDER
        config_path.write_text(json.dumps(config, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        if os.name != "nt":
            os.chmod(config_path, 0o600)
        secret_before = secret_path.read_bytes()
        access_before = (self.root / "config" / "p7-04-access.json").read_bytes()
        ui3.initialize_private_access(self.root, credential_id=access.credential_id)
        migrated = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertEqual(migrated["interaction_provider"], ui3.UI4_PROVIDER)
        self.assertEqual(secret_before, secret_path.read_bytes())
        self.assertEqual(access_before, (self.root / "config" / "p7-04-access.json").read_bytes())

    def test_listener_is_strictly_ipv4_loopback_and_non_privileged(self):
        self.assertEqual(ui3._listener("127.0.0.1", 8765), ("127.0.0.1", 8765))
        for host in ("0.0.0.0", "localhost", "::1", "192.0.2.10"):
            with self.subTest(host=host), self.assertRaises(ui3.UI3BoundaryError):
                ui3._listener(host, 8765)
        for port in (0, 80, 1023, 65536, True):
            with self.subTest(port=port), self.assertRaises(ui3.UI3BoundaryError):
                ui3._listener("127.0.0.1", port)

    def test_rotation_and_uninstall_material_do_not_modify_p704_state(self):
        self._grant_ui1_ui2()
        access = ui3.resolve_operator_access(self.root, self.credential_id)
        ui3.initialize_private_access(self.root, credential_id=access.credential_id)
        before = (self.root / "config" / "p7-04-access.json").read_bytes()
        old = (self.root / "secrets" / "p7-06-ui3" / "access.secret").read_text()
        rotated = ui3.rotate_access_secret(self.root)
        new = (self.root / "secrets" / "p7-06-ui3" / "access.secret").read_text()
        self.assertTrue(rotated["prior_sessions_invalidated"])
        self.assertNotEqual(old, new)
        ui3.remove_private_material(self.root)
        self.assertEqual(before, (self.root / "config" / "p7-04-access.json").read_bytes())
        self.assertTrue((self.root / "secrets" / "p7-04" / f"{self.credential_id}.secret").is_file())
        self.assertFalse((self.root / "config" / "p7-06-ui3.json").exists())

    def test_ui4_preflight_does_not_activate_ui2_canonical_mutation_provider(self):
        text = pathlib.Path(ui3.__file__).read_text(encoding="utf-8")
        self.assertIn("interaction_provider=lambda _interaction_id: None", text)
        self.assertIn("UI4_PROVIDER", text)
        self.assertIn("ui4.PREFLIGHT_PATH", text)
        self.assertIn("ui4.RUN_PATH", text)
        self.assertIn("HttpOnly; SameSite=Strict; Path=/", text)
        self.assertNotIn('"organizational_authority_provided":True', text)
        self.assertNotIn('"consequential_approval_provided":True', text)
        self.assertNotIn("GovernedInteractionCase(", text)
        self.assertEqual(ui4.PREFLIGHT_ID, "p7-06-ui4:first-real-owner-preflight")


if __name__ == "__main__":
    unittest.main()
