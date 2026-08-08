from __future__ import annotations

import ast
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "arvectum_os_ref"


class R10OperatorActionEntrypointGuardTests(unittest.TestCase):
    def test_package_modules_do_not_bypass_operator_safety_for_p405_action_adapter(self) -> None:
        """Future cross-capability modules must not call the lower-level P4.05 action adapter directly."""

        allowed = {"execution_action_experience.py", "operator_safety.py"}
        protected_names = {
            "prepare_canonical_mutation_action",
            "execute_canonical_mutation_action",
        }
        offenders: list[str] = []

        for path in sorted(PACKAGE_ROOT.glob("*.py")):
            if path.name in allowed:
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            imported: set[str] = set()
            called: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    if node.module.endswith("execution_action_experience"):
                        imported.update(alias.name for alias in node.names)
                elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    called.add(node.func.id)
            if protected_names.intersection(imported | called):
                offenders.append(path.name)

        self.assertEqual(
            offenders,
            [],
            "operator-facing package code must compose consequential P4.05 actions through "
            "operator_safety.py so current source-access freshness is rechecked",
        )


if __name__ == "__main__":
    unittest.main()
