import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from arvectum_os_ref.identity import Identity
import p7_04_persistent_access as p704
import p7_07_guarded_operational_entrypoint as guard
import p7_07_persistent_tender_operator_contour as p707


SAFE_BRIDGE = '''"""bounded product bridge"""
from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from arvectum_os_ref.integration_adapters import IntegrationAdapters

@dataclass(frozen=True, slots=True)
class ArvectumOSBridge:
    adapters: IntegrationAdapters

    def resolve_document(self, *, request: Any, governed_versions: Any, admitted: Any, artifact_id: Any) -> Any:
        """delegate"""
        return self.adapters.capabilities.resolve_document(
            request=request,
            governed_versions=governed_versions,
            admitted=admitted,
            artifact_id=artifact_id,
        )
'''


class P707GuardedOperationalEntrypointTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.access_root = self.base / "access"
        self.org = Identity("organization", "p7-07-guard-org", "platform")
        self.human = Identity("principal", "p7-07-guard-owner", self.org.value)
        p704.initialize_access_store(self.access_root, self.org)
        p704.register_principal(self.access_root, self.human, kind="human")

    def tearDown(self):
        self.tmp.cleanup()

    def _product_repo(self, source: str) -> Path:
        repo = self.base / "product"
        bridge = repo / p707.PRODUCT_BRIDGE_RELATIVE_PATH
        bridge.parent.mkdir(parents=True, exist_ok=True)
        bridge.write_text(source, encoding="utf-8")
        return repo

    def _active(self, operation: str, prefix: str):
        return guard._active_grants(
            self.access_root,
            operation=operation,
            resource_prefix=prefix,
        )

    def test_safe_bridge_shape_is_accepted(self):
        repo = self._product_repo(SAFE_BRIDGE)
        digest = guard.validate_product_bridge(repo)
        self.assertEqual(len(digest), 64)

    def test_executable_top_level_bridge_behavior_is_rejected_before_import(self):
        repo = self._product_repo(SAFE_BRIDGE + "\nprint('effect')\n")
        with self.assertRaisesRegex(guard.P707GuardError, "top-level"):
            guard.validate_product_bridge(repo)

    def test_resolve_document_with_extra_effect_is_rejected(self):
        unsafe = SAFE_BRIDGE.replace(
            '        """delegate"""\n        return self.adapters.capabilities.resolve_document(',
            '        """delegate"""\n        open("side-effect", "w").write("x")\n        return self.adapters.capabilities.resolve_document(',
        )
        repo = self._product_repo(unsafe)
        with self.assertRaisesRegex(guard.P707GuardError, "pure delegation"):
            guard.validate_product_bridge(repo)

    def test_failed_low_level_setup_cleans_new_setup_and_read_grants(self):
        read_resource = p707.READ_RESOURCE_PREFIX + "a" * 64

        def failing_setup(**_kwargs):
            p704.grant_access(
                self.access_root,
                self.human,
                operation=p707.SETUP_ACCESS_OPERATION,
                resource=p707.SETUP_ACCESS_RESOURCE,
                access_paths=(p707.ACCESS_PATH,),
            )
            p704.grant_access(
                self.access_root,
                self.human,
                operation=p707.READ_ACCESS_OPERATION,
                resource=read_resource,
                access_paths=(p707.ACCESS_PATH,),
            )
            raise RuntimeError("simulated post-grant setup failure")

        with patch.object(p707, "run_setup", side_effect=failing_setup):
            with self.assertRaisesRegex(RuntimeError, "simulated post-grant"):
                guard.guarded_setup(access_root=self.access_root)

        self.assertEqual(
            self._active(p707.SETUP_ACCESS_OPERATION, p707.SETUP_ACCESS_RESOURCE),
            set(),
        )
        self.assertEqual(
            self._active(p707.READ_ACCESS_OPERATION, p707.READ_RESOURCE_PREFIX),
            set(),
        )

    def test_successful_setup_keeps_new_exact_read_grant_but_no_setup_grant(self):
        read_resource = p707.READ_RESOURCE_PREFIX + "b" * 64
        expected = SimpleNamespace(status="PASS_ADMITTED_AND_CONFIGURED")

        def successful_setup(**_kwargs):
            setup_gid = p704.grant_access(
                self.access_root,
                self.human,
                operation=p707.SETUP_ACCESS_OPERATION,
                resource=p707.SETUP_ACCESS_RESOURCE,
                access_paths=(p707.ACCESS_PATH,),
            )
            p704.grant_access(
                self.access_root,
                self.human,
                operation=p707.READ_ACCESS_OPERATION,
                resource=read_resource,
                access_paths=(p707.ACCESS_PATH,),
            )
            p704.revoke_grant(self.access_root, setup_gid)
            return expected

        with patch.object(p707, "run_setup", side_effect=successful_setup):
            result = guard.guarded_setup(access_root=self.access_root)

        self.assertIs(result, expected)
        self.assertEqual(
            self._active(p707.SETUP_ACCESS_OPERATION, p707.SETUP_ACCESS_RESOURCE),
            set(),
        )
        self.assertEqual(
            len(self._active(p707.READ_ACCESS_OPERATION, p707.READ_RESOURCE_PREFIX)),
            1,
        )

    def test_stale_preexisting_setup_grant_blocks_retry(self):
        p704.grant_access(
            self.access_root,
            self.human,
            operation=p707.SETUP_ACCESS_OPERATION,
            resource=p707.SETUP_ACCESS_RESOURCE,
            access_paths=(p707.ACCESS_PATH,),
        )
        with patch.object(p707, "run_setup") as low_level:
            with self.assertRaisesRegex(guard.P707GuardError, "pre-existing active"):
                guard.guarded_setup(access_root=self.access_root)
        low_level.assert_not_called()


if __name__ == "__main__":
    unittest.main()
