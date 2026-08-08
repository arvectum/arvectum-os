from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import unittest


class P408BoundedProductEntryDemoTests(unittest.TestCase):
    def test_demo_renders_exact_contract_backed_product_entry_without_route_contract(self) -> None:
        reference_root = Path(__file__).parents[1]
        demo = reference_root / "examples" / "p4_08_bounded_product_entry_demo.py"
        env = os.environ.copy()
        env["PYTHONPATH"] = str(reference_root)
        completed = subprocess.run(
            [sys.executable, str(demo)],
            cwd=reference_root,
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        html = completed.stdout
        self.assertIn("Arvectum OS Workspace", html)
        self.assertIn("Entry context: Product bounded-review-product", html)
        self.assertIn("p4-08-bounded-review-product-v0.1.0", html)
        self.assertIn("Bounded product task", html)
        self.assertIn("Declared shared capability entries: CAP-001, CAP-002", html)
        self.assertIn("context only", html)
        self.assertIn("R10 operator-safety guard", html)
        self.assertNotIn("href=", html)
        self.assertNotIn("http://", html)
        self.assertNotIn("https://", html)
        self.assertNotIn("authorized=true", html.lower())


if __name__ == "__main__":
    unittest.main()
