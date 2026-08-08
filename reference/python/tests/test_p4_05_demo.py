import importlib.util
import unittest
from pathlib import Path


class P405StaticDemoTests(unittest.TestCase):
    def test_static_demo_builds_without_framework_or_server(self) -> None:
        path = Path(__file__).resolve().parents[1] / "examples" / "p4_05_governed_execution_demo.py"
        spec = importlib.util.spec_from_file_location("p4_05_governed_execution_demo", path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        html = module.build_demo()
        self.assertIn("P4.05 bounded Governed Execution", html)
        self.assertIn("Awaiting required gates", html)
        self.assertIn("Ready governed action context", html)
        self.assertNotIn("<form", html.lower())
        self.assertNotIn("onclick=", html.lower())


if __name__ == "__main__":
    unittest.main()
