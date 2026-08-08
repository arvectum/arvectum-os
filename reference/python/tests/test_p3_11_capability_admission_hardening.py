from __future__ import annotations

import ast
from pathlib import Path
import unittest


TEST_ROOT = Path(__file__).resolve().parent
PYTHON_ROOT = TEST_ROOT.parent
SOURCE_ROOT = PYTHON_ROOT / "arvectum_os_ref"
REPO_ROOT = TEST_ROOT.parents[2]
DOCS_ROOT = REPO_ROOT / "docs"

CAPABILITY_IDS = ("CAP-001", "CAP-002", "CAP-003", "CAP-004")

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

CONSUMER_LAYER_MODULES = {
    "cross_capability_enforcement",
    "product_capability_consumption",
    "shared_capability_reuse",
}

ADR_TRIGGER_IMPORT_ROOTS = {
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
    "elasticsearch",
    "opensearchpy",
    "qdrant_client",
    "pinecone",
    "chromadb",
    "weaviate",
    "neo4j",
    "grpc",
    "fastapi",
    "flask",
    "django",
    "pydantic",
    "msgpack",
    "avro",
    "protobuf",
    "requests",
    "httpx",
    "socket",
    "subprocess",
}


class P311CapabilityAdmissionHardeningTests(unittest.TestCase):
    """Guards the bounded P3.11 lifecycle/ADR/refactoring disposition."""

    @staticmethod
    def _section(text: str, start: str, end: str) -> str:
        return text.split(start, 1)[1].split(end, 1)[0]

    @staticmethod
    def _tree(path: Path) -> ast.Module:
        return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    @classmethod
    def _import_roots(cls, path: Path) -> set[str]:
        roots: set[str] = set()
        for node in ast.walk(cls._tree(path)):
            if isinstance(node, ast.Import):
                roots.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                roots.add(node.module.split(".", 1)[0])
        return roots

    @classmethod
    def _local_imports(cls, path: Path) -> set[str]:
        imported: set[str] = set()
        for node in ast.walk(cls._tree(path)):
            if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
                imported.add(node.module.split(".", 1)[0])
        return imported

    def test_catalog_records_exact_retained_incubating_set_after_p3_11(self) -> None:
        catalog = (
            DOCS_ROOT / "catalogs" / "PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md"
        ).read_text(encoding="utf-8")
        summary = self._section(
            catalog,
            "## 2. Current capability summary",
            "## 3. Retained boundaries",
        )
        rows = {
            capability_id: next(
                line
                for line in summary.splitlines()
                if line.startswith(f"| `{capability_id}` |")
            )
            for capability_id in CAPABILITY_IDS
        }

        self.assertEqual(set(rows), set(CAPABILITY_IDS))
        for capability_id, row in rows.items():
            with self.subTest(capability=capability_id):
                self.assertIn("| `Incubating` | `Provisional` |", row)
                self.assertIn("P3.11 PASS", row)
                self.assertNotIn("| `Active` |", row)

    def test_bounded_consumer_product_contracts_remain_provisional_evidence(self) -> None:
        for filename in (
            "P3-08-BOUNDED-CONSUMER-PRODUCT-CONTRACT.md",
            "P3-09-DISTINCT-BOUNDED-CONSUMER-PRODUCT-CONTRACT.md",
        ):
            with self.subTest(contract=filename):
                contract = (DOCS_ROOT / "contracts" / filename).read_text(encoding="utf-8")
                self.assertIn("Status: `Provisional`", contract)
                self.assertIn("Version: `0.1.0`", contract)
                self.assertNotIn("Status: `Stable`", contract)

    def test_phase_3_modules_still_select_no_adr_triggering_mechanism(self) -> None:
        for module_name in PHASE_3_MODULES:
            imports = self._import_roots(SOURCE_ROOT / module_name)
            selected = imports.intersection(ADR_TRIGGER_IMPORT_ROOTS)
            with self.subTest(module=module_name):
                self.assertEqual(
                    selected,
                    set(),
                    f"{module_name} crossed a reviewed P3.11 ADR trigger: {selected}",
                )

    def test_semantic_owners_remain_independent_of_consumer_composition_harnesses(self) -> None:
        for module_name in SEMANTIC_OWNER_MODULES:
            imports = self._local_imports(SOURCE_ROOT / module_name)
            with self.subTest(module=module_name):
                self.assertTrue(CONSUMER_LAYER_MODULES.isdisjoint(imports))

    def test_package_root_remains_provisional_not_public_platform_contract(self) -> None:
        path = SOURCE_ROOT / "__init__.py"
        docstring = ast.get_docstring(self._tree(path)) or ""
        self.assertIn("provisional", docstring.lower())
        self.assertIn("not a public platform contract", docstring.lower())

    def test_canonical_p3_11_review_records_bounded_decision(self) -> None:
        review = (
            DOCS_ROOT
            / "reviews"
            / "P3-11-capability-admission-adr-refactoring-hardening-review.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Status: `Complete`", review)
        self.assertIn("retain exactly `CAP-001` through `CAP-004`", review)
        self.assertIn("**ADR decision:** no new ADR proposal is justified", review)
        self.assertIn("Result: **`No material refactor justified.`**", review)
        self.assertIn("no `Active` promotion", review)
        self.assertIn("P3.12 — Phase 3 / M3 closure review", review)


if __name__ == "__main__":
    unittest.main()
