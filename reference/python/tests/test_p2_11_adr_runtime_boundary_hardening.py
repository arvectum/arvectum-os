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

DURABLE_OR_TRANSPORT_ROOTS = {
    "sqlalchemy",
    "psycopg",
    "psycopg2",
    "sqlite3",
    "redis",
    "kafka",
    "confluent_kafka",
    "pika",
    "aio_pika",
    "kombu",
    "celery",
    "nats",
    "grpc",
    "requests",
    "httpx",
}


class P211AdrRuntimeBoundaryHardeningTests(unittest.TestCase):
    """Guards the explicit P2.11 decision that current runtime seams remain provisional."""

    @staticmethod
    def _tree(module_name: str) -> ast.Module:
        path = PACKAGE_ROOT / module_name
        return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    @staticmethod
    def _local_imports(tree: ast.Module) -> set[str]:
        result: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
                result.add(node.module.split(".", 1)[0])
        return result

    @staticmethod
    def _external_import_roots(tree: ast.Module) -> set[str]:
        result: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                result.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                result.add(node.module.split(".", 1)[0])
        return result

    def test_semantic_owner_runtime_still_selects_no_durable_store_or_transport(self) -> None:
        for module_name in CORE_RUNTIME_MODULES:
            with self.subTest(module=module_name):
                imports = self._external_import_roots(self._tree(module_name))
                self.assertTrue(DURABLE_OR_TRANSPORT_ROOTS.isdisjoint(imports))

    def test_runtime_consistency_owns_logical_commit_without_projection_or_product_boundary_coupling(self) -> None:
        imports = self._local_imports(self._tree("runtime_consistency.py"))
        self.assertIn("event_provenance", imports)
        self.assertIn("governed_execution", imports)
        self.assertNotIn("portability_runtime", imports)
        self.assertNotIn("product_contract", imports)
        self.assertNotIn("runtime", imports)

    def test_portability_projection_boundary_cannot_depend_on_mutation_runtime(self) -> None:
        imports = self._local_imports(self._tree("portability_runtime.py"))
        self.assertNotIn("runtime_consistency", imports)
        self.assertNotIn("governed_execution", imports)
        self.assertNotIn("runtime", imports)
        self.assertNotIn("reference_runtime_adapters", imports)
        self.assertNotIn("reference_scenario", imports)

        source = (PACKAGE_ROOT / "portability_runtime.py").read_text(encoding="utf-8")
        self.assertIn("non-authoritative", source)
        self.assertIn("internal", source)
        self.assertIn("provisional", source)

    def test_product_contract_boundary_has_no_hidden_event_persistence_or_runtime_state_dependency(self) -> None:
        imports = self._local_imports(self._tree("product_contract.py"))
        forbidden = {
            "event_provenance",
            "runtime_consistency",
            "portability_runtime",
            "runtime",
            "reference_runtime_adapters",
            "reference_scenario",
        }
        self.assertTrue(forbidden.isdisjoint(imports))

    def test_no_repository_or_delivery_abstraction_is_normalized_before_an_adr_trigger(self) -> None:
        forbidden_fragments = (
            "repository",
            "unitofwork",
            "unit_of_work",
            "eventstore",
            "event_store",
            "outbox",
            "inbox",
            "publisher",
            "subscriber",
            "messagebroker",
            "message_broker",
        )
        for module_name in CORE_RUNTIME_MODULES:
            tree = self._tree(module_name)
            declared_names = {
                node.name.lower()
                for node in ast.walk(tree)
                if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
            }
            with self.subTest(module=module_name):
                self.assertFalse(
                    any(fragment in name for fragment in forbidden_fragments for name in declared_names),
                    "durable repository/Event-delivery abstraction requires a fresh ADR-gate assessment",
                )


if __name__ == "__main__":
    unittest.main()
