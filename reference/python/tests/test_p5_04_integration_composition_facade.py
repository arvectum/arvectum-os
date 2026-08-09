from __future__ import annotations

import ast
from dataclasses import fields, replace
from datetime import datetime, timezone
import inspect
import unittest

import arvectum_os_ref.integration_composition as facade_module
import bounded_product_ref.integration_journeys as product_journeys
from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.governed_execution import GovernedGateKind
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.integration_composition import (
    IntegrationCompositionContinuityError,
    compose_integration_facade,
)
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAPABILITY_CONTRACT_VERSION,
    OP_RESOLVE_DOCUMENT,
    CapabilityConsumptionRequest,
)
from arvectum_os_ref.product_contract import ProductRuntimeInteraction
from arvectum_os_ref.product_contract_resolution import (
    DependencyCompatibilityDecision,
    DependencySupportDisposition,
    GovernedDependencyVersionEvidence,
    ProductContractResolutionContinuityError,
    UnsupportedDependencyResolutionError,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import (
    OperationSideEffectClass,
    WorkflowDefinition,
    WorkflowLifecycle,
    WorkflowOperation,
)
from arvectum_os_ref.workspace_shell import PresentationAuthority, WorkspaceShellState
from bounded_product_ref.contract import (
    GOVERNED_RUNTIME_CONTRACT_VERSION,
    GOVERNED_RUNTIME_DEPENDENCY,
    OP_RECORD_TASK_DECISION,
    PRODUCT_TASK_AUTHORITY_SCOPE,
    PRODUCT_TASK_SEMANTIC_TYPE,
    PRODUCT_VERSION,
    build_p4_08_product_contract,
    product_id_for,
)
from bounded_product_ref.integration_journeys import (
    enter_facade_read_journey,
    start_facade_action_journey,
)


UTC = timezone.utc


class P504IntegrationCompositionFacadeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "p5-04-developer", "platform"))
        self.actor = ActorContext(self.principal, self.org)
        self.product_id = product_id_for(self.actor)
        self.contract = build_p4_08_product_contract(
            actor=self.actor,
            created_at=self._time(0),
        )
        self.access = AccessRequest(
            actor=self.actor,
            purpose="bounded-product-review",
            required_right="read",
            allowed_classifications=("internal",),
        )
        self.document_request = CapabilityConsumptionRequest(
            organization=self.org,
            product_id=self.product_id,
            product_version=PRODUCT_VERSION,
            dependency_id=CAP_001_DOCUMENT_ARTIFACT,
            dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
            operation_name=OP_RESOLVE_DOCUMENT,
            access=self.access,
        )

    def _time(self, minute: int) -> datetime:
        return datetime(2026, 8, 9, 13, minute, tzinfo=UTC)

    def _supported_versions(self) -> tuple[GovernedDependencyVersionEvidence, ...]:
        return tuple(
            GovernedDependencyVersionEvidence(
                dependency_id=dependency.dependency_id,
                contract_version=dependency.contract_version,
                disposition=DependencySupportDisposition.SUPPORTED,
                governance_reference=(
                    "test-governed-provider-evidence:"
                    f"{dependency.dependency_id.namespace}:"
                    f"{dependency.dependency_id.value}:"
                    f"{dependency.contract_version}"
                ),
            )
            for dependency in self.contract.dependencies
        )

    def _facade(self, *, governed_versions=None, effective_product_contract=None):
        return compose_integration_facade(
            contract=self.contract,
            actor=self.actor,
            effective_product_contract=(
                self.contract.version_pin
                if effective_product_contract is None
                else effective_product_contract
            ),
            governed_versions=(
                self._supported_versions()
                if governed_versions is None
                else governed_versions
            ),
        )

    def _record(
        self,
        *,
        subject_id: Identity,
        version_id: Identity,
        semantic_type: str,
        authority_scope: str,
        lifecycle_status: str,
        provenance_refs: tuple[Identity, ...],
    ) -> CanonicalRecord:
        return CanonicalRecord(
            subject_id=subject_id,
            version_id=version_id,
            semantic_type=semantic_type,
            schema_version="1",
            organization=self.org,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=authority_scope,
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=self._time(1),
            provenance_refs=provenance_refs,
            integrity_metadata=(("representation", "p5.04-facade-test"),),
            payload=(),
            lifecycle_status=lifecycle_status,
        )

    def _runtime_interaction(self) -> ProductRuntimeInteraction:
        task_subject = Identity("product-task", "task-1", "org-a")
        task_record = self._record(
            subject_id=task_subject,
            version_id=Identity("product-task-version", "task-1-v1", "org-a"),
            semantic_type=PRODUCT_TASK_SEMANTIC_TYPE,
            authority_scope=PRODUCT_TASK_AUTHORITY_SCOPE,
            lifecycle_status="Open",
            provenance_refs=(self.principal.principal_id, self.product_id),
        )
        workflow_record = self._record(
            subject_id=Identity("workflow-subject", "p5-04-task-decision", "org-a"),
            version_id=Identity("workflow-version", "p5-04-task-decision-v1", "org-a"),
            semantic_type="platform.workflow",
            authority_scope="platform.workflow/definition",
            lifecycle_status=WorkflowLifecycle.APPROVED.value,
            provenance_refs=(self.principal.principal_id, task_subject),
        )
        workflow = WorkflowDefinition(
            record=workflow_record,
            operations=(
                WorkflowOperation(
                    semantic_name=OP_RECORD_TASK_DECISION,
                    target_subject_id=task_subject,
                    target_semantic_type=PRODUCT_TASK_SEMANTIC_TYPE,
                    side_effect_classes=(OperationSideEffectClass.CANONICAL_MUTATION,),
                ),
            ),
        )
        return ProductRuntimeInteraction(
            organization=self.org,
            product_id=self.product_id,
            product_version=PRODUCT_VERSION,
            dependency_id=GOVERNED_RUNTIME_DEPENDENCY,
            dependency_contract_version=GOVERNED_RUNTIME_CONTRACT_VERSION,
            workflow=workflow,
            operation_name=OP_RECORD_TASK_DECISION,
            material_inputs=(task_record,),
            required_gates=(
                GovernedGateKind.AUTHORIZATION,
                GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
                GovernedGateKind.DATA_GOVERNANCE,
                GovernedGateKind.CONSEQUENTIAL_APPROVAL,
            ),
        )

    def test_facade_composes_exact_p502_and_p503_evidence(self) -> None:
        facade = self._facade()

        self.assertEqual(facade.context.organization, self.org)
        self.assertEqual(facade.context.actor, self.actor)
        self.assertEqual(facade.context.product_id, self.product_id)
        self.assertEqual(facade.context.product_version, PRODUCT_VERSION)
        self.assertEqual(facade.context.product_contract, self.contract.version_pin)
        self.assertEqual(
            facade.declaration_evidence.product_contract,
            self.contract.version_pin,
        )
        self.assertEqual(
            facade.compatibility_evidence.product_contract,
            self.contract.version_pin,
        )
        self.assertTrue(facade.compatibility_evidence.is_compatible)
        self.assertTrue(
            all(
                item.decision is DependencyCompatibilityDecision.COMPATIBLE
                for item in facade.compatibility_evidence.evaluations
            )
        )

    def test_unsupported_dependency_fails_before_facade_composition(self) -> None:
        governed_versions = self._supported_versions()[1:]
        with self.assertRaises(UnsupportedDependencyResolutionError):
            self._facade(governed_versions=governed_versions)

    def test_effective_product_contract_version_drift_fails_before_composition(self) -> None:
        stale_pin = replace(
            self.contract.version_pin,
            version_id=Identity(
                "product-contract-version",
                "p4-08-bounded-review-product-v0.0.9",
                self.contract.version_pin.version_id.scope,
            ),
        )
        with self.assertRaises(ProductContractResolutionContinuityError):
            self._facade(effective_product_contract=stale_pin)

    def test_j1_capability_admission_is_exact_and_delegated(self) -> None:
        facade = self._facade()
        admission = facade.admit_capability(
            self.document_request,
            governed_versions=self._supported_versions(),
        )

        self.assertEqual(admission.product_contract_version_id, self.contract.record.version_id)
        self.assertEqual(admission.product_id, self.product_id)
        self.assertEqual(admission.dependency_id, CAP_001_DOCUMENT_ARTIFACT)
        self.assertEqual(admission.dependency_contract_version, CAPABILITY_CONTRACT_VERSION)
        self.assertEqual(admission.operation_name, OP_RESOLVE_DOCUMENT)

    def test_j1_dependency_version_cannot_drift_after_facade_composition(self) -> None:
        drifted = replace(self.document_request, dependency_contract_version="9.9.9")
        with self.assertRaises(IntegrationCompositionContinuityError):
            self._facade().admit_capability(
                drifted,
                governed_versions=self._supported_versions(),
            )

    def test_workspace_entry_is_non_authoritative_and_pins_exact_contract(self) -> None:
        workspace = self._facade().open_workspace()

        self.assertIsInstance(workspace, WorkspaceShellState)
        self.assertEqual(workspace.organization, self.org)
        self.assertEqual(workspace.actor, self.actor)
        self.assertEqual(workspace.presentation_authority, PresentationAuthority.NON_AUTHORITATIVE)
        self.assertIsNotNone(workspace.product_context)
        self.assertEqual(workspace.product_context.product_id, self.product_id)
        self.assertEqual(
            workspace.product_context.product_contract_version_id,
            self.contract.record.version_id,
        )

    def test_product_j1_journey_uses_only_facade_and_preserves_entry_evidence(self) -> None:
        entry = enter_facade_read_journey(
            facade=self._facade(),
            capability_requests=(self.document_request,),
            governed_versions=self._supported_versions(),
        )

        self.assertIsInstance(entry.workspace, WorkspaceShellState)
        self.assertEqual(len(entry.capability_admissions), 1)
        self.assertEqual(
            entry.capability_admissions[0].product_contract_version_id,
            self.contract.record.version_id,
        )

    def test_j2_governed_execution_preserves_exact_contract_and_unsatisfied_gates(self) -> None:
        facade = self._facade()
        interaction = self._runtime_interaction()

        execution = facade.start_governed_execution(
            interaction=interaction,
            execution_id=Identity("execution-subject", "p5-04-task-1", "org-a"),
            version_id=Identity("execution-version", "p5-04-task-1-v1", "org-a"),
            created_at=self._time(2),
            governed_versions=self._supported_versions(),
        )

        self.assertEqual(execution.product_contract, self.contract.version_pin)
        self.assertEqual(execution.initiating_actor, self.actor)
        self.assertEqual(execution.required_gates, interaction.required_gates)
        self.assertFalse(execution.gate_decisions)

    def test_product_j2_journey_reaches_governed_execution_only_through_facade(self) -> None:
        interaction = self._runtime_interaction()
        execution = start_facade_action_journey(
            facade=self._facade(),
            interaction=interaction,
            execution_id=Identity("execution-subject", "p5-04-task-2", "org-a"),
            version_id=Identity("execution-version", "p5-04-task-2-v1", "org-a"),
            created_at=self._time(3),
            governed_versions=self._supported_versions(),
        )

        self.assertEqual(execution.product_contract, self.contract.version_pin)
        self.assertFalse(execution.gate_decisions)

    def test_facade_context_and_evidence_do_not_become_authority_decisions(self) -> None:
        facade = self._facade()
        field_sets = (
            {item.name for item in fields(facade.context)},
            {item.name for item in fields(facade.declaration_evidence)},
            {item.name for item in fields(facade.compatibility_evidence)},
        )
        for field_set in field_sets:
            for forbidden in (
                "authentication",
                "authorization",
                "permission",
                "organizational_authority",
                "approval",
                "capability_lifecycle",
                "active",
            ):
                self.assertNotIn(forbidden, field_set)

    def test_product_journey_module_has_one_platform_import_boundary(self) -> None:
        source = inspect.getsource(product_journeys)
        tree = ast.parse(source)
        platform_imports = tuple(
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
            and node.module is not None
            and node.module.startswith("arvectum_os_ref")
        )
        self.assertEqual(platform_imports, ("arvectum_os_ref.integration_composition",))

    def test_facade_remains_internal_provisional_and_does_not_select_public_stack(self) -> None:
        source = inspect.getsource(facade_module).lower()
        self.assertIn("internal", source)
        self.assertIn("provisional", source)
        self.assertIn("stable/public", source)
        self.assertIn("validate_product_contract_declaration", source)
        self.assertIn("resolve_product_contract_dependencies", source)
        self.assertIn("validate_capability_consumption", source)
        self.assertIn("open_workspace_shell", source)
        self.assertIn("start_product_governed_execution", source)
        self.assertNotIn("bounded_product_ref", source)

        for forbidden in (
            "import fastapi",
            "import requests",
            "import grpc",
            "import socket",
            "import yaml",
            "import json",
            "protobuf",
            "openapi",
        ):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
