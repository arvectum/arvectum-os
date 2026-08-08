from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import unittest


class P407MemoryKnowledgeSearchDemoTests(unittest.TestCase):
    def test_static_demo_renders_epistemic_and_derived_discovery_semantics(self) -> None:
        reference_root = Path(__file__).parents[1]
        demo = reference_root / "examples" / "p4_07_memory_knowledge_search_demo.py"
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
        self.assertIn("Arvectum OS P4.07 Memory / Knowledge / Search", html)
        self.assertIn("Observation", html)
        self.assertIn("Organizational Memory", html)
        self.assertIn("Knowledge Candidate", html)
        self.assertIn("Validated Knowledge", html)
        self.assertIn("delivery-knowledge-v1", html)
        self.assertIn("Derived discovery/projection", html)
        self.assertIn("Projection status", html)
        self.assertIn("Search match/order is a discovery signal only", html)
        self.assertIn("Promotion available here</dt><dd>no", html)
        self.assertNotIn("http://", html)
        self.assertNotIn("https://", html)
        self.assertNotIn("ranking_score", html)


if __name__ == "__main__":
    unittest.main()
