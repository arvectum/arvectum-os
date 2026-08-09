from __future__ import annotations

import ast
from pathlib import Path
import unittest


TEST_ROOT = Path(__file__).resolve().parent
PYTHON_ROOT = TEST_ROOT.parent
PLATFORM_ROOT = PYTHON_ROOT / "arvectum_os_ref"
PRODUCT_ROOT = PYTHON_ROOT / "bounded_product_ref"
EXTENSION_ROOT = PYTHON_ROOT / "evidence_extension_ref"

INTEGRATION_MODULES = (
    "product_contract_declaration.py",
    "product_contract_resolution.py",
    "integration_composition.py",
    "integration_scaffolding.py",
    "integration_evidence.py",
    "integration_adapters.py",
)

PUBLIC_OR_DURABLE_TRIGGER_IMPORT_ROOTS = {
    "fastapi",
    "starlette",
    "flask",
    "django",
    "graphql",
    "grpc",
    "requests",
    "httpx",
    "socket",
    "subprocess",
    "importlib_metadata",
    "pkg_resources",
    "entrypoints",
    "protobuf",
    "google",
    "avro",
    "msgpack",
    "yaml",
    "marshmallow",
    "pydantic",
}

DYNAMIC_EXTENSION_TOKENS = (
    "importlib.import_module",
    "entry_points(",
    "pkg_resources",
    "plugin_registry",
    "extension_registry",
    "load_plugin",
    "load_extension",
)

PUBLIC_COMPATIBILITY_TOKENS = (
    "stable public sdk",
    "public api version",
    "wire compatibility",
    "backward compatibility guarantee",
    "package compatibility guarantee",
)


class P511CompatibilityAdrPublicBoundaryHardeningReviewTests(unittest.TestCase):
    """Executable guards for the bounded P5.11 no-ADR/no-public-boundary disposition."""

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

    def test_integration_surface_remains_internal_and_not_root_exported(self) -> None:
        root_init = (PLATFORM_ROOT / "__init__.py").read_text(encoding="utf-8")
        for token in (
            "IntegrationCompositionFacade",
            "IntegrationAdapters",
            "IntegrationCapabilityAdapter",
            "IntegrationWorkspaceAdapter",
            "LocalIntegrationHarness",
            "compose_integration_facade",
            "compose_integration_adapters",
            "compose_workspace_adapter",
        ):
            with self.subTest(token=token):
                self.assertNotIn(token, root_init)

        adapters = (PLATFORM_ROOT / "integration_adapters.py").read_text(encoding="utf-8")
        composition = (PLATFORM_ROOT / "integration_composition.py").read_text(encoding="utf-8")
        self.assertIn("internal/provisional", adapters)
        self.assertIn("internal/provisional", composition)
        self.assertIn("do not establish a Stable/public SDK/API", adapters)

    def test_no_language_package_distribution_boundary_is_selected(self) -> None:
        for filename in ("pyproject.toml", "setup.py", "setup.cfg"):
            with self.subTest(filename=filename):
                self.assertFalse(
                    (PYTHON_ROOT / filename).exists(),
                    f"{filename} would require an explicit P5.11 package/distribution disposition",
                )

        product_sources = tuple(PRODUCT_ROOT.glob("*.py")) + tuple(EXTENSION_ROOT.glob("*.py"))
        self.assertTrue(product_sources)
        for path in product_sources:
            source = path.read_text(encoding="utf-8")
            self.assertNotIn("pkg_resources", source)
            self.assertNotIn("importlib.metadata", source)

    def test_no_public_api_wire_or_serialization_contract_is_selected(self) -> None:
        for module_name in INTEGRATION_MODULES:
            path = PLATFORM_ROOT / module_name
            selected = self._import_roots(path).intersection(PUBLIC_OR_DURABLE_TRIGGER_IMPORT_ROOTS)
            with self.subTest(module=module_name):
                self.assertEqual(
                    selected,
                    set(),
                    f"{module_name} crossed a reviewed public/durable mechanism trigger: {selected}",
                )

        integration_source = "\n".join(
            (PLATFORM_ROOT / module_name).read_text(encoding="utf-8")
            for module_name in INTEGRATION_MODULES
        ).casefold()
        for token in PUBLIC_COMPATIBILITY_TOKENS:
            with self.subTest(token=token):
                self.assertNotIn(token, integration_source)

    def test_no_plugin_or_extension_registry_runtime_is_selected(self) -> None:
        integration_source = "\n".join(
            (PLATFORM_ROOT / module_name).read_text(encoding="utf-8")
            for module_name in INTEGRATION_MODULES
        )
        for token in DYNAMIC_EXTENSION_TOKENS:
            with self.subTest(token=token):
                self.assertNotIn(token, integration_source)

    def test_compatibility_remains_exact_governed_evidence_not_version_range_inference(self) -> None:
        resolution = (PLATFORM_ROOT / "product_contract_resolution.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("GovernedDependencyVersionEvidence", resolution)
        self.assertIn("VersionMismatch", resolution)
        self.assertIn("Unsupported", resolution)
        self.assertIn("Deprecated", resolution)
        self.assertIn("Retired", resolution)
        self.assertIn("No fallback version is selected automatically", resolution)
        self.assertNotIn("from packaging", resolution)
        self.assertNotIn("import packaging", resolution)
        self.assertNotIn("semantic_version", resolution)

        adapters = (PLATFORM_ROOT / "integration_adapters.py").read_text(encoding="utf-8")
        self.assertIn("validate_product_contract_declaration", adapters)
        self.assertIn("facade.declaration_evidence", adapters)

    def test_scaffolding_and_generated_code_do_not_become_compatibility_boundaries(self) -> None:
        scaffolding = (PLATFORM_ROOT / "integration_scaffolding.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("internal/provisional", scaffolding)
        self.assertIn("readable", scaffolding.casefold())
        self.assertNotIn("autogenerated", scaffolding.casefold())
        self.assertNotIn("generated file", scaffolding.casefold())

    def test_integration_remains_in_process_without_deployable_service_topology(self) -> None:
        integration_source = "\n".join(
            (PLATFORM_ROOT / module_name).read_text(encoding="utf-8")
            for module_name in INTEGRATION_MODULES
        )
        for token in (
            "FastAPI(",
            "Flask(",
            "grpc.server",
            "HTTPServer(",
            "uvicorn",
            "gunicorn",
            "listen(",
        ):
            with self.subTest(token=token):
                self.assertNotIn(token, integration_source)

    def test_product_contracts_remain_provisional_and_not_stable(self) -> None:
        for path in (PRODUCT_ROOT / "contract.py", EXTENSION_ROOT / "contract.py"):
            with self.subTest(path=path.as_posix()):
                source = path.read_text(encoding="utf-8")
                self.assertIn("ProductContractLifecycle.PROVISIONAL", source)
                self.assertNotIn("ProductContractLifecycle.STABLE", source)
                self.assertIn("public", source.casefold())
                self.assertIn("stable", source.casefold())

    def test_no_stable_design_system_contract_is_created_by_phase5_integration(self) -> None:
        integration_source = "\n".join(
            (PLATFORM_ROOT / module_name).read_text(encoding="utf-8")
            for module_name in INTEGRATION_MODULES
        ).casefold()
        for token in (
            "design system",
            "component library",
            "css framework",
            "stable component",
        ):
            with self.subTest(token=token):
                self.assertNotIn(token, integration_source)


if __name__ == "__main__":
    unittest.main()
