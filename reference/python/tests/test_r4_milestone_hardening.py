from __future__ import annotations

import ast
from pathlib import Path
import unittest


TEST_ROOT = Path(__file__).resolve().parent
PACKAGE_ROOT = TEST_ROOT.parent / "arvectum_os_ref"

CORE_RUNTIME_MODULES = (
    "canonical.py",
    "canonical_lineage.py",
    "relationships.py",
    "governed_execution.py",
    "event_provenance.py",
    "runtime_consistency.py",
    "product_contract.py",
    "portability_runtime.py",
)

HISTORICAL_COMPOSITION_MODULES = {
    "runtime",
    "reference_runtime_adapters",
    "reference_scenario",
}

P2_SEMANTIC_OWNER_EXPORTS = {
    "CanonicalLineage",
    "TypedRelationshipLineage",
    "GovernedExecutionContext",
    "RuntimeConsistencyState",
    "ProductContract",
    "PortabilityPackage",
    "RuntimeComposition",
    "RuntimeOperations",
}


class R4MilestoneHardeningTests(unittest.TestCase):
    """Final Phase 2 code-health guards before P2.11/P2.12 closure reviews."""

    @staticmethod
    def _tree(module_name: str) -> ast.Module:
        path = PACKAGE_ROOT / module_name
        return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    @staticmethod
    def _imported_local_modules(tree: ast.Module) -> set[str]:
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
                imported.add(node.module.split(".", 1)[0])
        return imported

    def test_core_runtime_semantic_owners_do_not_depend_on_historical_p201_composition(self) -> None:
        for module_name in CORE_RUNTIME_MODULES:
            with self.subTest(module=module_name):
                imports = self._imported_local_modules(self._tree(module_name))
                self.assertTrue(HISTORICAL_COMPOSITION_MODULES.isdisjoint(imports))

    def test_package_root_remains_provisional_and_does_not_promote_p2_runtime_surface(self) -> None:
        path = PACKAGE_ROOT / "__init__.py"
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        docstring = ast.get_docstring(tree) or ""
        self.assertIn("provisional", docstring.lower())
        self.assertIn("not a public platform contract", docstring.lower())

        exported: set[str] = set()
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            if not any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
                continue
            self.assertIsInstance(node.value, (ast.List, ast.Tuple))
            for element in node.value.elts:
                if isinstance(element, ast.Constant) and isinstance(element.value, str):
                    exported.add(element.value)

        self.assertTrue(P2_SEMANTIC_OWNER_EXPORTS.isdisjoint(exported))

    def test_core_runtime_does_not_introduce_process_network_or_unsafe_deserialization_dependencies(self) -> None:
        forbidden_roots = {
            "subprocess",
            "socket",
            "requests",
            "httpx",
            "urllib",
            "pickle",
            "shelve",
            "marshal",
            "multiprocessing",
        }
        for module_name in CORE_RUNTIME_MODULES:
            tree = self._tree(module_name)
            imported_roots: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported_roots.update(alias.name.split(".", 1)[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                    imported_roots.add(node.module.split(".", 1)[0])
            with self.subTest(module=module_name):
                self.assertTrue(forbidden_roots.isdisjoint(imported_roots))

    def test_core_runtime_contains_no_dynamic_code_execution_calls(self) -> None:
        forbidden_calls = {"eval", "exec", "compile", "__import__"}
        for module_name in CORE_RUNTIME_MODULES:
            tree = self._tree(module_name)
            calls = {
                node.func.id
                for node in ast.walk(tree)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            }
            with self.subTest(module=module_name):
                self.assertTrue(forbidden_calls.isdisjoint(calls))

    def test_runtime_consistency_state_is_not_exposed_as_root_level_public_surface(self) -> None:
        root_source = (PACKAGE_ROOT / "__init__.py").read_text(encoding="utf-8")
        self.assertNotIn("RuntimeConsistencyState", root_source)
        consistency_source = (PACKAGE_ROOT / "runtime_consistency.py").read_text(encoding="utf-8")
        self.assertIn("not a durable transaction/store", consistency_source)

    def test_core_runtime_has_no_implicit_gate_allow_all_or_auto_approval_api(self) -> None:
        forbidden_names = {
            "allow_all_gates",
            "approve_all_gates",
            "auto_approve",
            "automatic_approval",
            "bypass_gates",
        }
        for module_name in CORE_RUNTIME_MODULES:
            tree = self._tree(module_name)
            defined_names = {
                node.name
                for node in ast.walk(tree)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            }
            with self.subTest(module=module_name):
                self.assertTrue(forbidden_names.isdisjoint(defined_names))

    def test_core_runtime_keeps_public_framework_and_serialization_choices_unselected(self) -> None:
        forbidden_roots = {
            "fastapi",
            "flask",
            "django",
            "pydantic",
            "grpc",
            "msgpack",
            "avro",
            "protobuf",
        }
        for module_name in CORE_RUNTIME_MODULES:
            tree = self._tree(module_name)
            imported_roots: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported_roots.update(alias.name.split(".", 1)[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                    imported_roots.add(node.module.split(".", 1)[0])
            with self.subTest(module=module_name):
                self.assertTrue(forbidden_roots.isdisjoint(imported_roots))


if __name__ == "__main__":
    unittest.main()
