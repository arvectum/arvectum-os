from __future__ import annotations

import ast
from pathlib import Path
import unittest


TEST_ROOT = Path(__file__).resolve().parent
PACKAGE_ROOT = TEST_ROOT.parent / "arvectum_os_ref"

PHASE_3_MODULES = (
    "document_artifact_governance.py",
    "memory_knowledge_governance.py",
    "search_index_projection.py",
    "audit_reconstruction_support.py",
    "cross_capability_enforcement.py",
    "product_capability_consumption.py",
    "shared_capability_reuse.py",
)

SEMANTIC_OWNER_MODULES = (
    "document_artifact_governance.py",
    "memory_knowledge_governance.py",
    "search_index_projection.py",
    "audit_reconstruction_support.py",
)

PHASE_3_ROOT_EXPORTS = {
    "AdmittedDocumentVersion",
    "ArtifactContent",
    "ValidatedKnowledge",
    "RetrievalProjection",
    "SearchProjection",
    "SearchHit",
    "AuditReconstructionView",
    "AccessRequest",
    "CapabilityConsumptionRequest",
    "ProductCapabilityAdmission",
    "BoundedConsumerComposition",
    "SharedCapabilityReuseProof",
    "consume_document",
    "consume_knowledge",
    "consume_search",
    "consume_search_source",
    "consume_reconstruction",
    "prove_shared_capability_reuse",
}


class R8Phase3MilestoneHardeningTests(unittest.TestCase):
    """Final Phase 3 code-health guards before P3.11/P3.12 closure reviews."""

    @staticmethod
    def _tree(module_name: str) -> ast.Module:
        path = PACKAGE_ROOT / module_name
        return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    @staticmethod
    def _local_imports(tree: ast.Module) -> set[str]:
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
                imported.add(node.module.split(".", 1)[0])
        return imported

    @staticmethod
    def _import_roots(tree: ast.Module) -> set[str]:
        roots: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                roots.add(node.module.split(".", 1)[0])
        return roots

    def test_phase_3_dependency_direction_keeps_semantic_owners_above_consumer_harnesses(self) -> None:
        consumer_layers = {
            "cross_capability_enforcement",
            "product_capability_consumption",
            "shared_capability_reuse",
        }
        for module_name in SEMANTIC_OWNER_MODULES:
            with self.subTest(module=module_name):
                self.assertTrue(
                    consumer_layers.isdisjoint(self._local_imports(self._tree(module_name)))
                )

        cross_imports = self._local_imports(self._tree("cross_capability_enforcement.py"))
        self.assertNotIn("product_capability_consumption", cross_imports)
        self.assertNotIn("shared_capability_reuse", cross_imports)

        product_imports = self._local_imports(self._tree("product_capability_consumption.py"))
        self.assertNotIn("shared_capability_reuse", product_imports)

    def test_package_root_remains_provisional_and_does_not_promote_phase_3_surface(self) -> None:
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
            if not any(
                isinstance(target, ast.Name) and target.id == "__all__"
                for target in node.targets
            ):
                continue
            self.assertIsInstance(node.value, (ast.List, ast.Tuple))
            for element in node.value.elts:
                if isinstance(element, ast.Constant) and isinstance(element.value, str):
                    exported.add(element.value)

        self.assertTrue(PHASE_3_ROOT_EXPORTS.isdisjoint(exported))

    def test_phase_3_modules_do_not_introduce_process_network_or_unsafe_deserialization(self) -> None:
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
        for module_name in PHASE_3_MODULES:
            with self.subTest(module=module_name):
                self.assertTrue(
                    forbidden_roots.isdisjoint(self._import_roots(self._tree(module_name)))
                )

    def test_phase_3_modules_contain_no_dynamic_code_execution_calls(self) -> None:
        forbidden_calls = {"eval", "exec", "compile", "__import__"}
        for module_name in PHASE_3_MODULES:
            calls = {
                node.func.id
                for node in ast.walk(self._tree(module_name))
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            }
            with self.subTest(module=module_name):
                self.assertTrue(forbidden_calls.isdisjoint(calls))

    def test_phase_3_modules_have_no_implicit_authority_or_gate_bypass_helpers(self) -> None:
        forbidden_names = {
            "allow_all_gates",
            "approve_all_gates",
            "auto_approve",
            "automatic_approval",
            "bypass_gates",
            "grant_all_permissions",
            "assume_authority",
        }
        for module_name in PHASE_3_MODULES:
            defined_names = {
                node.name
                for node in ast.walk(self._tree(module_name))
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            }
            with self.subTest(module=module_name):
                self.assertTrue(forbidden_names.isdisjoint(defined_names))

    def test_phase_3_keeps_public_framework_and_stable_serialization_choices_unselected(self) -> None:
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
        for module_name in PHASE_3_MODULES:
            with self.subTest(module=module_name):
                self.assertTrue(
                    forbidden_roots.isdisjoint(self._import_roots(self._tree(module_name)))
                )

    def test_cap004_fail_closed_security_remediation_remains_semantic_owner_evidence(self) -> None:
        path = TEST_ROOT / "test_p3_07_cross_capability_enforcement.py"
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        test_names = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
        }
        self.assertIn(
            "test_cap004_missing_or_unknown_evidence_constraints_fail_closed",
            test_names,
        )
        self.assertIn(
            "test_cap004_rejects_malformed_evidence_constraints",
            test_names,
        )


if __name__ == "__main__":
    unittest.main()
