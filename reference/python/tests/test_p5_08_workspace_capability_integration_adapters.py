from __future__ import annotations

import ast
from dataclasses import fields
from datetime import datetime, timezone
import inspect
import unittest

import arvectum_os_ref.integration_adapters as adapter_module
import bounded_product_ref.integration_adapter_journey as product_journey
from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.integration_adapters import compose_integration_adapters
from arvectum_os_ref.integration_composition import IntegrationCompositionEvidenceRequiredError
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAPABILITY_CONTRACT_VERSION,
    OP_RESOLVE_DOCUMENT,
    CapabilityConsumptionRequest,
)
from arvectum_os_ref.product_contract import ProductContractScopeError
from arvectum_os_ref.product_contract_resolution import (
    DependencySupportDisposition,
    GovernedDependencyVersionEvidence,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import (
    ExactVersionNavigationReference,
    PresentationAuthority,
    SubjectNavigationReference,
    WorkspaceDestination,
)
from bounded_product_ref.contract import (
    PRODUCT_VERSION,
    build_p4_08_product_contract,
    product_id_for,
)
from bounded_product_ref.integration_adapter_journey import enter_adapter_read_journey


UTC = timezone.utc


class P508WorkspaceCapabilityIntegrationAdaptersTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "p5-08-developer", "platform"))
        self.actor = ActorContext(self.principal, self.org)
        self.product_id = product_id_for(self.actor)
        self.contract = build_p4_08_product_contract(
            actor=self.actor,
            created_at=datetime(2026, 8, 9, 15, 0, tzinfo=UTC),
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

    def _supported_versions(self) -> tuple[GovernedDependencyVersionEvidence, ...]:
        return tuple(
            GovernedDependencyVersionEvidence(
                dependency_id=dependency.dependency_id,
                contract_version=dependency.contract_version,
                disposition=DependencySupportDisposition.SUPPORTED,
                governance_reference=(
                    "p5.08-current-provider-evidence:"
                    f"{dependency.dependency_id.namespace}:"
                    f"{dependency.dependency_id.value}:"
                    f"{dependency.contract_version}"
                ),
            )
            for dependency in self.contract.dependencies
        )

    def _adapters(self):
        return compose_integration_adapters(
            contract=self.contract,
            actor=self.actor,
            effective_product_contract=self.contract.version_pin,
            governed_versions=self._supported_versions(),
        )

    def test_adapter_composition_preserves_exact_facade_contract_context(self) -> None:
        adapters = self._adapters()

        self.assertEqual(adapters.facade.context.organization, self.org)
        self.assertEqual(adapters.facade.context.actor, self.actor)
        self.assertEqual(adapters.facade.context.product_id, self.product_id)
        self.assertEqual(adapters.facade.context.product_contract, self.contract.version_pin)
        self.assertIs(adapters.workspace.facade, adapters.facade)
        self.assertIs(adapters.capabilities.facade, adapters.facade)

    def test_workspace_adapter_remains_non_authoritative_and_pins_contract(self) -> None:
        workspace = self._adapters().workspace.open()

        self.assertEqual(workspace.presentation_authority, PresentationAuthority.NON_AUTHORITATIVE)
        self.assertEqual(workspace.organization, self.org)
        self.assertEqual(workspace.actor, self.actor)
        self.assertIsNotNone(workspace.product_context)
        self.assertEqual(
            workspace.product_context.product_contract_version_id,
            self.contract.record.version_id,
        )

    def test_workspace_adapter_navigates_subject_without_private_workspace_import_in_product(self) -> None:
        adapter = self._adapters().workspace
        workspace = adapter.open()
        subject = Identity("document-subject", "doc-p5-08", "org-a")

        next_state = adapter.navigate_subject(
            workspace,
            destination=WorkspaceDestination.DOCUMENTS,
            subject_id=subject,
        )

        self.assertIsInstance(next_state.current_reference, SubjectNavigationReference)
        self.assertEqual(next_state.current_reference.subject_id, subject)
        self.assertEqual(next_state.product_context, workspace.product_context)

    def test_workspace_adapter_navigates_exact_version_with_continuity(self) -> None:
        adapter = self._adapters().workspace
        workspace = adapter.open()
        subject = Identity("document-subject", "doc-p5-08", "org-a")
        version = Identity("document-version", "doc-p5-08-v1", "org-a")

        next_state = adapter.navigate_exact_version(
            workspace,
            destination=WorkspaceDestination.DOCUMENTS,
            subject_id=subject,
            version_id=version,
        )

        self.assertIsInstance(next_state.current_reference, ExactVersionNavigationReference)
        self.assertEqual(next_state.current_reference.subject_id, subject)
        self.assertEqual(next_state.current_reference.version_id, version)
        self.assertEqual(next_state.product_context.product_contract_version_id, self.contract.record.version_id)

    def test_workspace_adapter_rejects_cross_organization_identity_scope(self) -> None:
        adapter = self._adapters().workspace
        workspace = adapter.open()

        with self.assertRaises(ProductContractScopeError):
            adapter.navigate_subject(
                workspace,
                destination=WorkspaceDestination.DOCUMENTS,
                subject_id=Identity("document-subject", "foreign-doc", "org-b"),
            )

        with self.assertRaises(ProductContractScopeError):
            adapter.navigate_exact_version(
                workspace,
                destination=WorkspaceDestination.DOCUMENTS,
                subject_id=Identity("document-subject", "doc-p5-08", "org-a"),
                version_id=Identity("document-version", "foreign-doc-v1", "org-b"),
            )

    def test_capability_adapter_admission_reuses_current_facade_compatibility_gate(self) -> None:
        admission = self._adapters().capabilities.admit(
            self.document_request,
            governed_versions=self._supported_versions(),
        )

        self.assertEqual(admission.product_contract_version_id, self.contract.record.version_id)
        self.assertEqual(admission.product_id, self.product_id)
        self.assertEqual(admission.dependency_id, CAP_001_DOCUMENT_ARTIFACT)
        self.assertEqual(admission.operation_name, OP_RESOLVE_DOCUMENT)

    def test_capability_adapter_cannot_self_advance_without_current_provider_evidence(self) -> None:
        with self.assertRaises(IntegrationCompositionEvidenceRequiredError):
            self._adapters().capabilities.admit(
                self.document_request,
                governed_versions=None,
            )

    def test_product_adapter_journey_has_one_integration_facing_platform_import(self) -> None:
        source = inspect.getsource(product_journey)
        tree = ast.parse(source)
        platform_imports = tuple(
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
            and node.module is not None
            and node.module.startswith("arvectum_os_ref")
        )
        self.assertEqual(platform_imports, ("arvectum_os_ref.integration_adapters",))
        for forbidden in (
            "workspace_shell",
            "product_capability_consumption",
            "cross_capability_enforcement",
            "document_artifact_governance",
            "memory_knowledge_governance",
            "search_index_projection",
            "audit_reconstruction_support",
        ):
            self.assertNotIn(forbidden, source)

    def test_product_journey_reaches_workspace_and_admission_without_private_coupling(self) -> None:
        entry = enter_adapter_read_journey(
            adapters=self._adapters(),
            capability_requests=(self.document_request,),
            governed_versions=self._supported_versions(),
        )

        self.assertEqual(entry.workspace.presentation_authority, PresentationAuthority.NON_AUTHORITATIVE)
        self.assertEqual(len(entry.capability_admissions), 1)
        self.assertEqual(
            entry.capability_admissions[0].product_contract_version_id,
            self.contract.record.version_id,
        )

    def test_adapter_evidence_is_not_an_authority_or_lifecycle_decision(self) -> None:
        adapters = self._adapters()
        field_sets = (
            {field.name for field in fields(adapters)},
            {field.name for field in fields(adapters.workspace)},
            {field.name for field in fields(adapters.capabilities)},
        )
        for field_set in field_sets:
            for forbidden in (
                "authorization",
                "permission",
                "organizational_authority",
                "approval",
                "capability_lifecycle",
                "active",
            ):
                self.assertNotIn(forbidden, field_set)

    def test_adapter_module_remains_internal_provisional_and_stack_neutral(self) -> None:
        source = inspect.getsource(adapter_module).lower()
        self.assertIn("internal/provisional", source)
        self.assertIn("not a new semantic owner", source)
        self.assertIn("compose_integration_facade", source)
        self.assertIn("consume_document", source)
        self.assertIn("navigate_workspace", source)
        self.assertNotIn("bounded_product_ref", source)

        for forbidden in (
            "import fastapi",
            "import requests",
            "import grpc",
            "import socket",
            "import json",
            "import yaml",
            "protobuf",
            "openapi",
        ):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
