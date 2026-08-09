from __future__ import annotations

import ast
from dataclasses import fields, replace
from datetime import datetime, timezone
import inspect
import unittest

import arvectum_os_ref.integration_adapters as adapter_module
import arvectum_os_ref.integration_scaffolding as scaffolding_module
import bounded_product_ref.integration_adapter_journey as product_journey
import evidence_extension_ref.reconstruction_journey as extension_journey
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.integration_adapters import (
    IntegrationWorkspaceAdapter,
    compose_integration_adapters,
    compose_workspace_adapter,
)
from arvectum_os_ref.integration_scaffolding import (
    render_integration_entry_template,
    run_local_integration_harness,
)
from arvectum_os_ref.product_contract import (
    CanonicalAccessMode,
    ProductContractCanonicalAccessError,
    ProductContractLifecycle,
)
from arvectum_os_ref.product_contract_declaration import validate_product_contract_declaration
from arvectum_os_ref.product_contract_resolution import (
    DependencySupportDisposition,
    GovernedDependencyVersionEvidence,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from bounded_product_ref.contract import build_p4_08_product_contract
from evidence_extension_ref.contract import build_p5_09_product_contract


UTC = timezone.utc


class R15ReuseDeveloperExperienceRefactoringReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "r15-reviewer", "platform"))
        self.actor = ActorContext(self.principal, self.org)
        self.product_contract = build_p4_08_product_contract(
            actor=self.actor,
            created_at=datetime(2026, 8, 9, 17, 0, tzinfo=UTC),
        )
        self.extension_contract = build_p5_09_product_contract(
            actor=self.actor,
            created_at=datetime(2026, 8, 9, 17, 5, tzinfo=UTC),
        )

    def _supported_versions(self, contract) -> tuple[GovernedDependencyVersionEvidence, ...]:
        return tuple(
            GovernedDependencyVersionEvidence(
                dependency_id=dependency.dependency_id,
                contract_version=dependency.contract_version,
                disposition=DependencySupportDisposition.SUPPORTED,
                governance_reference=(
                    "r15-current-provider-evidence:"
                    f"{dependency.dependency_id.namespace}:"
                    f"{dependency.dependency_id.value}:"
                    f"{dependency.contract_version}"
                ),
            )
            for dependency in contract.dependencies
        )

    def _adapters(self, contract):
        return compose_integration_adapters(
            contract=contract,
            actor=self.actor,
            effective_product_contract=contract.version_pin,
            governed_versions=self._supported_versions(contract),
        )

    def test_shared_adapter_state_contains_only_two_consumer_core(self) -> None:
        adapters = self._adapters(self.extension_contract)
        field_names = tuple(item.name for item in fields(adapters))

        self.assertEqual(field_names, ("facade", "capabilities"))
        self.assertNotIn("workspace", field_names)
        self.assertIs(adapters.capabilities.facade, adapters.facade)

    def test_workspace_is_explicit_optional_binding_over_same_facade(self) -> None:
        adapters = self._adapters(self.product_contract)
        workspace_adapter = compose_workspace_adapter(adapters=adapters)

        self.assertIsInstance(workspace_adapter, IntegrationWorkspaceAdapter)
        self.assertIs(workspace_adapter.facade, adapters.facade)
        self.assertIs(adapters.workspace.facade, adapters.facade)
        self.assertIsNot(adapters.workspace, adapters.workspace)

    def test_consumers_share_adapter_module_but_only_product_opts_into_workspace(self) -> None:
        def platform_imports(module) -> tuple[str, ...]:
            tree = ast.parse(inspect.getsource(module))
            return tuple(
                node.module
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom)
                and node.module is not None
                and node.module.startswith("arvectum_os_ref")
            )

        self.assertEqual(platform_imports(product_journey), ("arvectum_os_ref.integration_adapters",))
        self.assertEqual(platform_imports(extension_journey), ("arvectum_os_ref.integration_adapters",))
        self.assertIn("compose_workspace_adapter", inspect.getsource(product_journey))
        self.assertNotIn("compose_workspace_adapter", inspect.getsource(extension_journey))
        self.assertNotIn("workspace", {item.name for item in fields(self._adapters(self.extension_contract))})

    def test_scaffold_teaches_proven_adapter_seam_not_lower_level_facade(self) -> None:
        template = render_integration_entry_template()
        tree = ast.parse(template.source)
        imports = tuple(
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
            and node.module is not None
            and node.module.startswith("arvectum_os_ref")
        )

        self.assertEqual(imports, ("arvectum_os_ref.integration_adapters",))
        self.assertIn("compose_workspace_adapter", template.source)
        self.assertNotIn("integration_composition", template.source)

        module_source = inspect.getsource(scaffolding_module)
        self.assertIn("compose_integration_adapters", module_source)
        self.assertIn("compose_workspace_adapter", module_source)

    def test_local_harness_preserves_shared_adapter_core_and_exact_contract(self) -> None:
        result = run_local_integration_harness(
            contract=self.product_contract,
            actor=self.actor,
            effective_product_contract=self.product_contract.version_pin,
            governed_versions=self._supported_versions(self.product_contract),
        )

        result_fields = tuple(item.name for item in fields(result))
        self.assertIn("adapters", result_fields)
        self.assertNotIn("facade", result_fields)
        self.assertIs(result.facade, result.adapters.facade)
        self.assertEqual(result.adapters.facade.context.product_contract, self.product_contract.version_pin)
        self.assertEqual(result.workspace.product_context.product_contract_version_id, self.product_contract.version_pin.version_id)

    def test_p5_09_f1_derived_read_distinction_is_preserved(self) -> None:
        extension_validation = validate_product_contract_declaration(contract=self.extension_contract)

        self.assertEqual(extension_validation.lifecycle, ProductContractLifecycle.PROVISIONAL)
        self.assertEqual(extension_validation.canonical_accesses, ())

        read_operation = self.product_contract.operations[0]
        changed_access = replace(
            read_operation.canonical_accesses[0],
            access_modes=(CanonicalAccessMode.WRITE,),
        )
        changed_operation = replace(read_operation, canonical_accesses=(changed_access,))
        changed_contract = replace(
            self.product_contract,
            operations=(changed_operation,) + self.product_contract.operations[1:],
        )
        with self.assertRaises(ProductContractCanonicalAccessError):
            validate_product_contract_declaration(contract=changed_contract)

    def test_refactoring_remains_internal_provisional_without_public_boundary_inflation(self) -> None:
        source = inspect.getsource(adapter_module).lower()

        self.assertIn("internal/provisional", source)
        self.assertIn("stable/public", source)
        self.assertIn("not new semantic owners", source)
        for forbidden in (
            "import fastapi",
            "import requests",
            "import grpc",
            "import socket",
            "import json",
            "import yaml",
            "protobuf",
            "openapi",
            "plugin registry",
            "extension registry",
        ):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
