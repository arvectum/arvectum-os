from __future__ import annotations

from pathlib import Path
import ast
import unittest

from arvectum_os_ref.authority_safe_ux import (
    AuthoritySafeActionLabel,
    AuthoritySafeUxState,
    consume_current_source_authorization,
)
from arvectum_os_ref.canonical_inspection import CurrentSourceAuthorization
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import (
    WorkspaceBlockedState,
    WorkspaceShellState,
    open_workspace_shell,
    render_workspace_shell_html,
)


REFERENCE_ROOT = Path(__file__).parents[1]
PLATFORM_ROOT = REFERENCE_ROOT / "arvectum_os_ref"
PRODUCT_ROOT = REFERENCE_ROOT / "bounded_product_ref"

FITNESS_DIMENSIONS = (
    "organization_isolation",
    "identity_attribution",
    "authorization_vs_organizational_authority",
    "canonical_vs_derived_state",
    "exact_version_visibility_and_reliance",
    "provenance_and_reconstruction_honesty",
    "product_contract_boundary_integrity",
    "document_artifact_authority_semantics",
    "knowledge_search_non_authority",
    "fail_closed_action_paths",
    "product_domain_neutrality",
    "accessibility_baseline",
    "deterministic_critical_state_testability",
    "presentation_portability_and_reversibility",
)


class P410WorkspaceArchitectureFitnessAccessibilityUsabilityTests(unittest.TestCase):
    def _read(self, root: Path, name: str) -> str:
        return (root / name).read_text(encoding="utf-8")

    def setUp(self) -> None:
        self.organization = OrganizationScope(
            Identity("organization", "org-p410", "platform")
        )
        self.other_organization = OrganizationScope(
            Identity("organization", "org-p410-other", "platform")
        )
        self.actor = ActorContext(
            Principal(Identity("principal", "operator-p410", "platform")),
            self.organization,
        )
        opened = open_workspace_shell(self.actor)
        self.assertIsInstance(opened, WorkspaceShellState)
        self.workspace = opened
        self.subject = Identity("record-subject", "subject-p410", "platform")
        self.decision_v1 = Identity(
            "authorization-decision-version", "p410-v1", "platform"
        )
        self.decision_v2 = Identity(
            "authorization-decision-version", "p410-v2", "platform"
        )

    def _decision(
        self,
        *,
        allowed: bool = True,
        organization: OrganizationScope | None = None,
        version: Identity | None = None,
    ) -> CurrentSourceAuthorization:
        return CurrentSourceAuthorization(
            organization=organization or self.organization,
            actor_actual_principal_id=self.actor.actual_principal.principal_id,
            resource_subject_id=self.subject,
            decision_version_id=version or self.decision_v1,
            allowed=allowed,
        )

    def test_all_fourteen_p4_10_fitness_dimensions_have_executable_guards(self) -> None:
        self.assertEqual(len(FITNESS_DIMENSIONS), 14)
        self.assertEqual(len(set(FITNESS_DIMENSIONS)), 14)

        evidence = {
            "organization_isolation": (
                "workspace_shell.py",
                "Actor and workspace Organization scope must match",
                "CONTEXT_SCOPE_MISMATCH",
            ),
            "identity_attribution": (
                "workspace_shell.py",
                "actual_principal",
                "represented_principal",
            ),
            "authorization_vs_organizational_authority": (
                "authority_safe_ux.py",
                "does not decide permissions",
                "Organizational Authority",
            ),
            "canonical_vs_derived_state": (
                "provenance_inspection.py",
                "DERIVED_NON_AUTHORITATIVE",
                "PROJECTION_ONLY",
            ),
            "exact_version_visibility_and_reliance": (
                "canonical_inspection.py",
                "displayed_version_id",
                "head_version_id",
            ),
            "provenance_and_reconstruction_honesty": (
                "provenance_inspection.py",
                "provenance_refs",
                "causation_refs",
            ),
            "document_artifact_authority_semantics": (
                "document_artifact_experience.py",
                "authoritative_source_text",
                "ExactRelianceAvailability",
            ),
            "knowledge_search_non_authority": (
                "memory_knowledge_search_experience.py",
                "DiscoveryAuthority",
                "Derived discovery/projection",
            ),
            "fail_closed_action_paths": (
                "operator_safety.py",
                "re-inspect before preparing the action",
                "execute_canonical_mutation_action",
            ),
            "accessibility_baseline": (
                "workspace_shell.py",
                'aria-current="page"',
                'role="alert"',
            ),
            "deterministic_critical_state_testability": (
                "authority_safe_ux.py",
                "REINSPECTION_REQUIRED",
                "NOT_AVAILABLE",
            ),
            "presentation_portability_and_reversibility": (
                "workspace_shell.py",
                "minimal inert HTML adapter",
                "Presentation state only; it is not authorization",
            ),
        }
        for dimension, (module_name, *tokens) in evidence.items():
            with self.subTest(dimension=dimension):
                source = self._read(PLATFORM_ROOT, module_name)
                for token in tokens:
                    self.assertIn(token, source)

        product_source = self._read(PRODUCT_ROOT, "task_composition.py")
        self.assertIn(
            "admission.product_contract_version_id == contract_version_id",
            product_source,
        )
        self.assertIn("prepare_operator_canonical_mutation_action(", product_source)
        self.assertIn("execute_operator_canonical_mutation_action(", product_source)

        platform_source = "\n".join(
            path.read_text(encoding="utf-8") for path in PLATFORM_ROOT.glob("*.py")
        )
        self.assertNotIn("product.bounded-review-task", platform_source)
        self.assertNotIn("p4.08.record-task-decision", platform_source)

        covered = set(evidence) | {
            "product_contract_boundary_integrity",
            "product_domain_neutrality",
        }
        self.assertEqual(covered, set(FITNESS_DIMENSIONS))

    def test_accessibility_baseline_is_textual_semantic_and_not_color_only(self) -> None:
        html = render_workspace_shell_html(self.workspace)
        self.assertIn("<main", html)
        self.assertIn("<h1>Arvectum OS Workspace</h1>", html)
        self.assertIn('aria-label="Workspace"', html)
        self.assertIn('aria-current="page"', html)
        self.assertIn("Organization:", html)
        self.assertIn("Actor:", html)
        self.assertIn("Presentation state only", html)
        self.assertIn("<button", html)
        self.assertNotIn("style=", html.casefold())

        blocked = open_workspace_shell(None)
        self.assertIsInstance(blocked, WorkspaceBlockedState)
        blocked_html = render_workspace_shell_html(blocked)
        self.assertIn('role="alert"', blocked_html)
        self.assertIn("Workspace unavailable", blocked_html)
        self.assertIn("Organization scope is unresolved", blocked_html)
        self.assertNotIn("<nav", blocked_html)
        self.assertNotIn("<button", blocked_html)

        for module_name in (
            "canonical_inspection.py",
            "provenance_inspection.py",
            "execution_action_experience.py",
            "document_artifact_experience.py",
            "memory_knowledge_search_experience.py",
        ):
            with self.subTest(module=module_name):
                source = self._read(PLATFORM_ROOT, module_name)
                self.assertIn("from html import escape", source)
                self.assertIn('role="alert"', source)

    def test_operator_can_distinguish_object_version_authority_action_and_reason(self) -> None:
        canonical_source = self._read(PLATFORM_ROOT, "canonical_inspection.py")
        for token in (
            "object_kind:",
            "subject_id:",
            "displayed_version_id:",
            "head_version_id:",
            "authority: AuthorityInspection",
            "status_text:",
        ):
            self.assertIn(token, canonical_source)

        execution_source = self._read(PLATFORM_ROOT, "execution_action_experience.py")
        for token in (
            "displayed_execution_version_id:",
            "action_readiness: ActionReadiness",
            "unresolved_gates:",
            "denied_gates:",
            "status_text:",
        ):
            self.assertIn(token, execution_source)

        ux_source = self._read(PLATFORM_ROOT, "authority_safe_ux.py")
        for token in (
            'REQUEST_ACTION = "Request governed action"',
            'REINSPECT = "Re-inspect current access"',
            'UNAVAILABLE = "Action unavailable"',
        ):
            self.assertIn(token, ux_source)

    def test_security_critical_visibility_states_are_deterministic_and_fail_closed(self) -> None:
        cases = (
            (),
            (self._decision(allowed=False),),
            (self._decision(), self._decision()),
            (self._decision(organization=self.other_organization),),
        )
        for decisions in cases:
            with self.subTest(decisions=decisions):
                result = consume_current_source_authorization(
                    workspace=self.workspace,
                    resource_subject_id=self.subject,
                    source_authorizations=decisions,
                    allow_derived_preview=True,
                )
                self.assertEqual(result.state, AuthoritySafeUxState.NOT_AVAILABLE)
                self.assertEqual(
                    result.action_label, AuthoritySafeActionLabel.UNAVAILABLE
                )
                self.assertFalse(result.governed_content_visible)
                self.assertFalse(result.protected_count_visible)
                self.assertFalse(result.derived_preview_visible)

        replaced = consume_current_source_authorization(
            workspace=self.workspace,
            resource_subject_id=self.subject,
            source_authorizations=(self._decision(version=self.decision_v2),),
            expected_decision_version_id=self.decision_v1,
            allow_derived_preview=True,
        )
        self.assertEqual(
            replaced.state, AuthoritySafeUxState.REINSPECTION_REQUIRED
        )
        self.assertEqual(replaced.action_label, AuthoritySafeActionLabel.REINSPECT)
        self.assertFalse(replaced.governed_content_visible)
        self.assertFalse(replaced.derived_preview_visible)

    def test_source_authorization_helper_reuse_remains_narrow_until_semantic_owners_can_be_preserved(self) -> None:
        reviewed_modules = (
            "canonical_inspection.py",
            "provenance_inspection.py",
            "execution_action_experience.py",
            "document_artifact_experience.py",
            "memory_knowledge_search_experience.py",
            "operator_safety.py",
        )
        for module_name in reviewed_modules:
            with self.subTest(module=module_name):
                source = self._read(PLATFORM_ROOT, module_name)
                self.assertIn("CurrentSourceAuthorization", source)
                self.assertNotIn("from .authority_safe_ux import", source)

        document_source = self._read(PLATFORM_ROOT, "document_artifact_experience.py")
        self.assertIn("resolve_document_for_access(", document_source)
        knowledge_source = self._read(
            PLATFORM_ROOT, "memory_knowledge_search_experience.py"
        )
        self.assertIn("freshness_state", knowledge_source)
        self.assertIn("allowed_classifications", knowledge_source)
        provenance_source = self._read(PLATFORM_ROOT, "provenance_inspection.py")
        self.assertIn("reconstruct_audit_for_access(", provenance_source)

    def test_product_contract_boundary_and_governed_action_choke_point_remain_intact(self) -> None:
        source = self._read(PRODUCT_ROOT, "task_composition.py")
        self.assertIn(
            "admission.product_contract_version_id == contract_version_id",
            source,
        )
        self.assertIn("request.access.actor != entry.workspace.actor", source)
        self.assertIn("request.organization != entry.workspace.organization", source)
        self.assertIn("prepare_operator_canonical_mutation_action(", source)
        self.assertIn("execute_operator_canonical_mutation_action(", source)
        self.assertNotIn(
            "from arvectum_os_ref.execution_action_experience import", source
        )

    def test_presentation_boundary_remains_reversible_and_technology_neutral(self) -> None:
        reviewed_paths = (
            PLATFORM_ROOT / "workspace_shell.py",
            PLATFORM_ROOT / "canonical_inspection.py",
            PLATFORM_ROOT / "provenance_inspection.py",
            PLATFORM_ROOT / "execution_action_experience.py",
            PLATFORM_ROOT / "document_artifact_experience.py",
            PLATFORM_ROOT / "memory_knowledge_search_experience.py",
            PLATFORM_ROOT / "authority_safe_ux.py",
            PRODUCT_ROOT / "task_composition.py",
        )
        imported_roots: set[str] = set()
        for path in reviewed_paths:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
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
            "react",
            "nextjs",
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
