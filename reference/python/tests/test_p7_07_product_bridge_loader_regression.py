import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

import p7_07_persistent_tender_operator_contour as p707


class P707ProductBridgeLoaderRegressionTests(unittest.TestCase):
    def test_real_dynamic_load_registers_slots_dataclass_module(self):
        with tempfile.TemporaryDirectory() as tmp:
            product_repo = Path(tmp)
            bridge_path = product_repo / p707.PRODUCT_BRIDGE_RELATIVE_PATH
            bridge_path.parent.mkdir(parents=True)
            source = '''from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ArvectumOSBridge:
    adapters: object
'''
            bridge_path.write_text(source, encoding="utf-8")
            module_name = (
                "arvectum_tender_agent_p707_bridge_"
                + hashlib.sha256(str(bridge_path.resolve()).encode()).hexdigest()[:12]
            )
            adapters = object()
            try:
                bridge, digest = p707._load_product_bridge(product_repo, adapters)
                self.assertIs(bridge.adapters, adapters)
                self.assertEqual(digest, hashlib.sha256(source.encode("utf-8")).hexdigest())
                self.assertEqual(bridge.__class__.__module__, module_name)
                self.assertIn(module_name, sys.modules)
                self.assertIs(sys.modules[module_name].ArvectumOSBridge, bridge.__class__)
            finally:
                sys.modules.pop(module_name, None)


if __name__ == "__main__":
    unittest.main()
