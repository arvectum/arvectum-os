from __future__ import annotations

from pathlib import Path
import ast
import unittest


REFERENCE_ROOT = Path(__file__).parents[1]
PLATFORM_ROOT = REFERENCE_ROOT / "arvectum_os_ref"
PRODUCT_ROOT = REFERENCE_ROOT / "bounded_product_ref"


class R11CompositionUsabilityRefactoringReviewTests(unittest.TestCase):
    def _read(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def test_product_domain_semantics_remain_outside_shared_platform_package(self) -> None:
        platform_source = "\n".join(
            self._read(path) for path in PLATFORM_ROOT.glob("*.py")
        )
        product_source = "\n".join(
            self._read(path) for path in PRODUCT_ROOT.glob("*.py")
        )

        for token in (
            "product.bounded-review-task",
            "p4.08.record-task-decision",
            "Needs review",
            "Ready to proceed",
            "Declined",
        ):
            with self.subTest(token=token):
                self.assertNotIn(token, platform_source)
                self.assertIn(token, product_source)

        self.assertNotIn("bounded_product_ref", platform_source)

    def test_product_composition_preserves_shared_surface_semantic_owners(self) -> None:
        source = self._read(PRODUCT_ROOT / "task_composition.py")

        self.assertIn("document: DocumentWorkspaceResult", source)
        self.assertIn("knowledge: KnowledgeWorkspaceResult", source)
        self.assertIn("inspect_document_workspace(", source)
        self.assertIn("inspect_knowledge_workspace(", source)

        for flattened_field in (
            "document_authority_mode:",
            "document_provenance:",
            "knowledge_freshness_state:",
            "knowledge_approval_state:",
            "knowledge_authority_mode:",
        ):
            with self.subTest(flattened_field=flattened_field):
                self.assertNotIn(flattened_field, source)

    def test_composed_surfaces_keep_version_authority_provenance_and_approval_distinct(self) -> None:
        document_source = self._read(
            PLATFORM_ROOT / "document_artifact_experience.py"
        )
        knowledge_source = self._read(
            PLATFORM_ROOT / "memory_knowledge_search_experience.py"
        )
        execution_source = self._read(
            PLATFORM_ROOT / "execution_action_experience.py"
        )

        for token in (
            "reference_basis: DocumentReferenceBasis",
            "displayed_version_id: Identity",
            "authority_mode: AuthorityMode",
            "authority_scope: str",
            "authoritative_source_text: str",
            "source_artifact_ids: tuple[Identity, ...]",
            "transformation: str | None",
            "exact_reliance: ExactRelianceAvailability",
        ):
            with self.subTest(document_token=token):
                self.assertIn(token, document_source)

        for token in (
            "role: LearningRole",
            "version_id: Identity | None",
            "provenance_refs: tuple[Identity, ...]",
            "freshness_state: str",
            "authority_mode: AuthorityMode | None",
            "validation_result: str | None",
            "approval_ref: Identity | None",
            "exact_reliance: ExactRelianceState",
        ):
            with self.subTest(knowledge_token=token):
                self.assertIn(token, knowledge_source)

        for token in (
            "kind: GovernedGateKind",
            "outcome: GovernedGateOutcome | None",
            "decision_version_id: Identity | None",
            "basis_ref: Identity | None",
            "workflow: GovernedVersionPin",
            "material_inputs: tuple[GovernedVersionPin, ...]",
            "product_contract: GovernedVersionPin | None",
            "unresolved_gates: tuple[GovernedGateKind, ...]",
            "denied_gates: tuple[GovernedGateKind, ...]",
        ):
            with self.subTest(execution_token=token):
                self.assertIn(token, execution_source)

    def test_product_contract_dependency_actor_and_task_continuity_remain_fail_closed(self) -> None:
        source = self._read(PRODUCT_ROOT / "task_composition.py")

        for guard in (
            "request.access.actor != entry.workspace.actor",
            "request.organization != entry.workspace.organization",
            "request.product_id != entry.task.product_id",
            "request.product_version != entry.task.product_version",
            "request.mechanism is not ProductBoundaryMechanism.DECLARED_PLATFORM_CONTRACT",
            "admission.dependency_contract_version == request.dependency_contract_version",
            "admission.product_contract_version_id == contract_version_id",
            "execution.product_contract.version_id != expected_contract",
            "execution.initiating_actor != entry.workspace.actor",
            "execution.operation_name != OP_RECORD_TASK_DECISION",
            "execution.material_inputs[0].subject_id != entry.task.task_id",
            "candidate.subject_id != entry.task.task_id",
        ):
            with self.subTest(guard=guard):
                self.assertIn(guard, source)

    def test_consequential_product_action_has_no_r10_or_governed_execution_bypass(self) -> None:
        source = self._read(PRODUCT_ROOT / "task_composition.py")
        platform_source = "\n".join(
            self._read(path) for path in PLATFORM_ROOT.glob("*.py")
        )

        self.assertIn("prepare_operator_canonical_mutation_action(", source)
        self.assertIn("execute_operator_canonical_mutation_action(", source)
        self.assertNotIn(
            "from arvectum_os_ref.execution_action_experience import", source
        )
        self.assertNotIn("prepare_canonical_mutation_action(", source)
        self.assertNotIn("execute_canonical_mutation_action(", source)
        self.assertNotIn("bounded_product_ref", platform_source)

    def test_repeated_source_access_matching_has_not_become_a_new_authorization_framework(self) -> None:
        reviewed_modules = (
            "canonical_inspection.py",
            "provenance_inspection.py",
            "execution_action_experience.py",
            "document_artifact_experience.py",
            "memory_knowledge_search_experience.py",
            "operator_safety.py",
        )

        for module_name in reviewed_modules:
            source = self._read(PLATFORM_ROOT / module_name)
            with self.subTest(module=module_name):
                self.assertIn("CurrentSourceAuthorization", source)
                self.assertIn("resource_subject_id", source)
                self.assertIn("actor_actual_principal_id", source)
                self.assertIn("represented_principal_id", source)
                self.assertIn("allowed", source)

        platform_names = {path.name for path in PLATFORM_ROOT.glob("*.py")}
        for speculative_owner in (
            "authorization_framework.py",
            "workspace_authorization.py",
            "presentation_policy_engine.py",
            "product_composition_framework.py",
        ):
            with self.subTest(speculative_owner=speculative_owner):
                self.assertNotIn(speculative_owner, platform_names)

    def test_composition_selects_no_durable_frontend_api_iam_or_storage_boundary(self) -> None:
        reviewed_paths = (
            PLATFORM_ROOT / "workspace_shell.py",
            PLATFORM_ROOT / "canonical_inspection.py",
            PLATFORM_ROOT / "provenance_inspection.py",
            PLATFORM_ROOT / "execution_action_experience.py",
            PLATFORM_ROOT / "document_artifact_experience.py",
            PLATFORM_ROOT / "memory_knowledge_search_experience.py",
            PLATFORM_ROOT / "operator_safety.py",
            PRODUCT_ROOT / "task_composition.py",
        )
        imported_roots: set[str] = set()
        for path in reviewed_paths:
            tree = ast.parse(self._read(path), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported_roots.update(
                        alias.name.split(".", 1)[0] for alias in node.names
                    )
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported_roots.add(node.module.split(".", 1)[0])

        for dependency in (
            "fastapi",
            "starlette",
            "flask",
            "django",
            "graphql",
            "grpc",
            "sqlalchemy",
            "redis",
            "celery",
            "kafka",
            "auth0",
            "keycloak",
        ):
            with self.subTest(dependency=dependency):
                self.assertNotIn(dependency, imported_roots)


if __name__ == "__main__":
    unittest.main()
