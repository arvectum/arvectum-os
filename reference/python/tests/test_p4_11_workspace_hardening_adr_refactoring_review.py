from __future__ import annotations

import ast
from pathlib import Path
import unittest

from arvectum_os_ref.authority_safe_ux import (
    AuthoritySafeActionLabel,
    AuthoritySafeUxState,
    consume_current_source_authorization,
)
from arvectum_os_ref.canonical_inspection import CurrentSourceAuthorization
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import WorkspaceShellState, open_workspace_shell


TEST_ROOT = Path(__file__).resolve().parent
PYTHON_ROOT = TEST_ROOT.parent
PLATFORM_ROOT = PYTHON_ROOT / "arvectum_os_ref"
PRODUCT_ROOT = PYTHON_ROOT / "bounded_product_ref"
REPO_ROOT = TEST_ROOT.parents[2]
DOCS_ROOT = REPO_ROOT / "docs"

PHASE_4_MODULES = (
    "workspace_shell.py",
    "canonical_inspection.py",
    "provenance_inspection.py",
    "execution_action_experience.py",
    "document_artifact_experience.py",
    "memory_knowledge_search_experience.py",
    "operator_safety.py",
    "authority_safe_ux.py",
)

ADR_TRIGGER_IMPORT_ROOTS = {
    "fastapi",
    "starlette",
    "flask",
    "django",
    "pydantic",
    "graphql",
    "grpc",
    "requests",
    "httpx",
    "sqlalchemy",
    "psycopg",
    "psycopg2",
    "sqlite3",
    "redis",
    "celery",
    "kafka",
    "confluent_kafka",
    "elasticsearch",
    "opensearchpy",
    "qdrant_client",
    "pinecone",
    "chromadb",
    "weaviate",
    "neo4j",
    "msgpack",
    "avro",
    "protobuf",
    "socket",
    "subprocess",
}

PRODUCT_DOMAIN_TOKENS = (
    "product.bounded-review-task",
    "p4.08.record-task-decision",
    "ProductTaskDisposition",
    "Needs review",
    "Ready to proceed",
)


class P411WorkspaceHardeningAdrRefactoringReviewTests(unittest.TestCase):
    """Guards the bounded P4.11 boundary/refactoring/ADR disposition."""

    def setUp(self) -> None:
        self.organization = OrganizationScope(
            Identity("organization", "org-p411", "platform")
        )
        self.actor = ActorContext(
            Principal(Identity("principal", "operator-p411", "platform")),
            self.organization,
        )
        opened = open_workspace_shell(self.actor)
        self.assertIsInstance(opened, WorkspaceShellState)
        self.workspace = opened
        self.subject = Identity("record-subject", "subject-p411", "platform")
        self.decision_v1 = Identity(
            "authorization-decision-version", "p411-v1", "platform"
        )
        self.decision_v2 = Identity(
            "authorization-decision-version", "p411-v2", "platform"
        )

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

    def _allow(self, version: Identity) -> CurrentSourceAuthorization:
        return CurrentSourceAuthorization(
            organization=self.organization,
            actor_actual_principal_id=self.actor.actual_principal.principal_id,
            resource_subject_id=self.subject,
            decision_version_id=version,
            allowed=True,
        )

    def test_r12_stale_authorization_continuity_remains_fixed(self) -> None:
        initial = consume_current_source_authorization(
            workspace=self.workspace,
            resource_subject_id=self.subject,
            source_authorizations=(self._allow(self.decision_v1),),
            allow_derived_preview=True,
        )
        self.assertEqual(initial.state, AuthoritySafeUxState.AVAILABLE)
        self.assertEqual(
            initial.source_authorization_decision_version_id, self.decision_v1
        )

        replaced = consume_current_source_authorization(
            workspace=self.workspace,
            resource_subject_id=self.subject,
            source_authorizations=(self._allow(self.decision_v2),),
            expected_decision_version_id=initial.source_authorization_decision_version_id,
            allow_derived_preview=True,
        )
        self.assertEqual(
            replaced.state, AuthoritySafeUxState.REINSPECTION_REQUIRED
        )
        self.assertEqual(replaced.action_label, AuthoritySafeActionLabel.REINSPECT)
        self.assertEqual(
            replaced.source_authorization_decision_version_id, self.decision_v1
        )
        self.assertNotEqual(
            replaced.source_authorization_decision_version_id, self.decision_v2
        )
        self.assertFalse(replaced.governed_content_visible)
        self.assertFalse(replaced.protected_count_visible)
        self.assertFalse(replaced.derived_preview_visible)

        repeated = consume_current_source_authorization(
            workspace=self.workspace,
            resource_subject_id=self.subject,
            source_authorizations=(self._allow(self.decision_v2),),
            expected_decision_version_id=replaced.source_authorization_decision_version_id,
            allow_derived_preview=True,
        )
        self.assertEqual(repeated.state, AuthoritySafeUxState.REINSPECTION_REQUIRED)
        self.assertEqual(
            repeated.source_authorization_decision_version_id, self.decision_v1
        )
        self.assertFalse(repeated.governed_content_visible)

    def test_presentation_domain_boundary_remains_domain_neutral(self) -> None:
        platform_source = "\n".join(
            (PLATFORM_ROOT / module_name).read_text(encoding="utf-8")
            for module_name in PHASE_4_MODULES
        )
        self.assertNotIn("bounded_product_ref", platform_source)
        for token in PRODUCT_DOMAIN_TOKENS:
            with self.subTest(token=token):
                self.assertNotIn(token, platform_source)

        product_source = (PRODUCT_ROOT / "task_composition.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("class ProductTaskDisposition", product_source)
        self.assertIn("from arvectum_os_ref.operator_safety import (", product_source)
        self.assertNotIn(
            "from arvectum_os_ref.execution_action_experience import", product_source
        )

    def test_shared_refactoring_does_not_collapse_semantic_owner_controls(self) -> None:
        reviewed = {
            "canonical_inspection.py": (
                "CurrentSourceAuthorization",
                "_matching_authorization(",
                "EffectiveResolutionStatus",
            ),
            "provenance_inspection.py": (
                "CurrentSourceAuthorization",
                "reconstruct_audit_for_access(",
                "EvidenceAvailability",
            ),
            "document_artifact_experience.py": (
                "CurrentSourceAuthorization",
                "resolve_document_for_access(",
                "HandlingConstraints",
            ),
            "memory_knowledge_search_experience.py": (
                "CurrentSourceAuthorization",
                "freshness_state",
                "allowed_classifications",
            ),
            "operator_safety.py": (
                "CurrentSourceAuthorization",
                "_same_current_source_access(",
                "expected_decision_version_id",
            ),
        }
        for module_name, tokens in reviewed.items():
            with self.subTest(module=module_name):
                source = (PLATFORM_ROOT / module_name).read_text(encoding="utf-8")
                self.assertNotIn("from .authority_safe_ux import", source)
                for token in tokens:
                    self.assertIn(token, source)

        ux_source = (PLATFORM_ROOT / "authority_safe_ux.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("does not evaluate purpose/right/classification policy", ux_source)
        self.assertIn("capability owners must continue", ux_source)

    def test_derived_state_remains_non_authoritative_and_rebuildable(self) -> None:
        provenance = (PLATFORM_ROOT / "provenance_inspection.py").read_text(
            encoding="utf-8"
        )
        knowledge = (PLATFORM_ROOT / "memory_knowledge_search_experience.py").read_text(
            encoding="utf-8"
        )
        shell = (PLATFORM_ROOT / "workspace_shell.py").read_text(encoding="utf-8")

        self.assertIn("DERIVED_NON_AUTHORITATIVE", provenance)
        self.assertIn("PROJECTION_ONLY", provenance)
        self.assertIn("Derived discovery/projection — non-authoritative", knowledge)
        self.assertIn("non-authoritative presentation", shell.casefold())
        self.assertIn("not a public SDK/API", shell)
        self.assertIn("durable read-model topology", shell)

    def test_phase_4_still_selects_no_adr_triggering_mechanism(self) -> None:
        reviewed_paths = tuple(PLATFORM_ROOT / name for name in PHASE_4_MODULES) + (
            PRODUCT_ROOT / "task_composition.py",
        )
        for path in reviewed_paths:
            selected = self._import_roots(path).intersection(ADR_TRIGGER_IMPORT_ROOTS)
            with self.subTest(path=path.name):
                self.assertEqual(
                    selected,
                    set(),
                    f"{path.name} crossed a reviewed P4.11 ADR trigger: {selected}",
                )

    def test_accessibility_and_operator_error_semantics_remain_explicit(self) -> None:
        shell = (PLATFORM_ROOT / "workspace_shell.py").read_text(encoding="utf-8")
        self.assertIn('role="alert"', shell)
        self.assertIn('aria-current="page"', shell)
        self.assertIn("from html import escape", shell)

        ux = (PLATFORM_ROOT / "authority_safe_ux.py").read_text(encoding="utf-8")
        for token in (
            'REQUEST_ACTION = "Request governed action"',
            'REINSPECT = "Re-inspect current access"',
            'UNAVAILABLE = "Action unavailable"',
        ):
            self.assertIn(token, ux)

        for module_name in (
            "canonical_inspection.py",
            "provenance_inspection.py",
            "execution_action_experience.py",
            "document_artifact_experience.py",
            "memory_knowledge_search_experience.py",
        ):
            with self.subTest(module=module_name):
                source = (PLATFORM_ROOT / module_name).read_text(encoding="utf-8")
                self.assertIn("from html import escape", source)
                self.assertIn('role="alert"', source)

    def test_product_contract_remains_provisional_and_no_stable_boundary_is_inferred(self) -> None:
        contract = (
            DOCS_ROOT / "contracts" / "P4-08-BOUNDED-PRODUCT-ENTRY-PRODUCT-CONTRACT.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Status: `Provisional`", contract)
        self.assertIn("Version: `0.1.0`", contract)
        self.assertNotIn("Status: `Stable`", contract)
        self.assertIn("No IAM/PDP/PEP provider", contract)
        self.assertIn("No database, object store, search technology, frontend framework", contract)


if __name__ == "__main__":
    unittest.main()
