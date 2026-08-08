from __future__ import annotations

import ast
from dataclasses import fields
from pathlib import Path
import unittest

from arvectum_os_ref.identity import Identity
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import (
    ExactVersionNavigationReference,
    SubjectNavigationReference,
    WorkspaceDestination,
    WorkspaceProductContext,
    WorkspaceShellState,
    navigate_workspace,
    open_workspace_shell,
    render_workspace_shell_html,
)


TEST_ROOT = Path(__file__).resolve().parent
PACKAGE_ROOT = TEST_ROOT.parent / "arvectum_os_ref"
WORKSPACE_MODULE = PACKAGE_ROOT / "workspace_shell.py"
PACKAGE_INIT = PACKAGE_ROOT / "__init__.py"
P402_TESTS = TEST_ROOT / "test_p4_02_workspace_shell.py"


class R9WorkspaceBoundaryReviewTests(unittest.TestCase):
    """Structural guards for the P4.01 + P4.02 workspace boundary."""

    @staticmethod
    def _tree(path: Path) -> ast.Module:
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

    @staticmethod
    def _root_exports() -> set[str]:
        tree = R9WorkspaceBoundaryReviewTests._tree(PACKAGE_INIT)
        exported: set[str] = set()
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            if not any(
                isinstance(target, ast.Name) and target.id == "__all__"
                for target in node.targets
            ):
                continue
            if not isinstance(node.value, (ast.List, ast.Tuple)):
                continue
            for element in node.value.elts:
                if isinstance(element, ast.Constant) and isinstance(element.value, str):
                    exported.add(element.value)
        return exported

    def setUp(self) -> None:
        self.organization = OrganizationScope(
            Identity("organization", "org-r9", "platform")
        )
        self.actor = ActorContext(
            Principal(Identity("principal", "operator-r9", "platform")),
            self.organization,
        )

    def test_workspace_surface_remains_internal_and_unexported(self) -> None:
        root_source = PACKAGE_INIT.read_text(encoding="utf-8")
        exported = self._root_exports()
        workspace_public_names = {
            "WorkspaceDestination",
            "WorkspaceShellState",
            "WorkspaceProductContext",
            "SubjectNavigationReference",
            "ExactVersionNavigationReference",
            "open_workspace_shell",
            "navigate_workspace",
            "render_workspace_shell_html",
        }

        self.assertTrue(workspace_public_names.isdisjoint(exported))
        self.assertNotIn("from .workspace_shell import", root_source)

    def test_workspace_shell_dependency_boundary_stays_presentation_only(self) -> None:
        tree = self._tree(WORKSPACE_MODULE)

        self.assertEqual(self._local_imports(tree), {"identity", "security"})

        forbidden_local_dependencies = {
            "canonical",
            "mutation",
            "execution",
            "gates",
            "events",
            "workflow",
            "document_artifact_governance",
            "memory_knowledge_governance",
            "search_index_projection",
            "audit_reconstruction_support",
            "product_capability_consumption",
            "shared_capability_reuse",
        }
        self.assertTrue(forbidden_local_dependencies.isdisjoint(self._local_imports(tree)))

    def test_workspace_shell_selects_no_public_transport_frontend_or_storage_stack(self) -> None:
        forbidden_roots = {
            "fastapi",
            "flask",
            "django",
            "starlette",
            "pydantic",
            "grpc",
            "requests",
            "httpx",
            "aiohttp",
            "socket",
            "urllib",
            "sqlalchemy",
            "sqlite3",
            "psycopg",
            "redis",
            "boto3",
            "jinja2",
            "msgpack",
            "avro",
            "protobuf",
        }

        self.assertTrue(
            forbidden_roots.isdisjoint(self._import_roots(self._tree(WORKSPACE_MODULE)))
        )

    def test_navigation_references_are_semantic_not_route_or_wire_contracts(self) -> None:
        subject_fields = {field.name for field in fields(SubjectNavigationReference)}
        version_fields = {field.name for field in fields(ExactVersionNavigationReference)}

        self.assertEqual(subject_fields, {"organization", "subject_id"})
        self.assertEqual(version_fields, {"organization", "subject_id", "version_id"})

        forbidden_transport_fields = {
            "url",
            "uri",
            "href",
            "route",
            "path",
            "query",
            "token",
            "session",
            "endpoint",
            "payload",
        }
        self.assertTrue(forbidden_transport_fields.isdisjoint(subject_fields))
        self.assertTrue(forbidden_transport_fields.isdisjoint(version_fields))

    def test_product_entry_context_remains_context_only_until_p4_08(self) -> None:
        context_fields = {field.name for field in fields(WorkspaceProductContext)}
        self.assertEqual(
            context_fields,
            {"organization", "product_id", "product_contract_version_id"},
        )
        self.assertTrue(
            {
                "authorized",
                "permissions",
                "organizational_authority",
                "approved",
                "contract_valid",
                "contract_status",
                "capabilities",
                "operations",
            }.isdisjoint(context_fields)
        )

        context = WorkspaceProductContext(
            organization=self.organization,
            product_id=Identity("product", "product-r9", "platform"),
            product_contract_version_id=Identity(
                "product-contract-version", "pc-r9", "org-r9"
            ),
        )
        state = open_workspace_shell(self.actor, product_context=context)
        self.assertIsInstance(state, WorkspaceShellState)
        self.assertIs(state.product_context, context)

    def test_presentation_navigation_cannot_enter_governed_mutation_or_gate_paths(self) -> None:
        tree = self._tree(WORKSPACE_MODULE)
        defined_calls = {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        forbidden_calls = {
            "execute_p1_06_canonical_mutation",
            "start_p1_04_execution",
            "evaluate_p1_05_gates",
            "admit_p1_05_ready_execution",
            "consume_document",
            "consume_knowledge",
            "consume_search",
            "consume_reconstruction",
        }
        self.assertTrue(forbidden_calls.isdisjoint(defined_calls))

        state = open_workspace_shell(self.actor)
        self.assertIsInstance(state, WorkspaceShellState)
        exact = ExactVersionNavigationReference(
            organization=self.organization,
            subject_id=Identity("subject", "subject-r9", "org-r9"),
            version_id=Identity("version", "version-r9", "org-r9"),
        )
        next_state = navigate_workspace(
            state,
            destination=WorkspaceDestination.RECORDS,
            reference=exact,
        )
        self.assertEqual(next_state.current_reference, exact)
        for forbidden_attribute in (
            "authorized",
            "permissions",
            "organizational_authority",
            "approved",
            "canonical_mutation",
            "execution_context",
            "gate_decision",
        ):
            with self.subTest(attribute=forbidden_attribute):
                self.assertFalse(hasattr(next_state, forbidden_attribute))

    def test_html_adapter_remains_inert_and_does_not_define_navigation_protocol(self) -> None:
        state = open_workspace_shell(self.actor)
        self.assertIsInstance(state, WorkspaceShellState)
        html = render_workspace_shell_html(state).lower()

        for forbidden_fragment in (
            "href=",
            "action=",
            "onclick=",
            "<script",
            "<form",
            "fetch(",
            "xmlhttprequest",
            "websocket",
            "/records",
            "/executions",
        ):
            with self.subTest(fragment=forbidden_fragment):
                self.assertNotIn(forbidden_fragment, html)

    def test_p4_02_negative_boundary_evidence_remains_present(self) -> None:
        tree = self._tree(P402_TESTS)
        test_names = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
        }
        required = {
            "test_unresolved_organization_fails_closed_without_default",
            "test_wrong_organization_navigation_reference_is_rejected",
            "test_subject_and_exact_version_references_remain_distinct",
            "test_exact_historical_version_is_preserved_without_head_redirect",
            "test_presentation_state_cannot_create_authorization_or_authority",
            "test_shell_navigation_has_no_counts_or_protected_content_inventory",
            "test_product_entry_context_is_scope_checked_and_non_authoritative",
            "test_rendered_shell_has_textual_context_and_no_route_contract",
        }
        self.assertTrue(required.issubset(test_names))


if __name__ == "__main__":
    unittest.main()
