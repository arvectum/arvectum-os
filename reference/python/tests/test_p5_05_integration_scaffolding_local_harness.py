from __future__ import annotations

import ast
from dataclasses import fields
from datetime import datetime, timezone
import inspect
import unittest

import arvectum_os_ref.integration_scaffolding as scaffolding_module
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.integration_scaffolding import (
    render_integration_entry_template,
    run_local_integration_harness,
)
from arvectum_os_ref.product_contract_resolution import (
    DependencySupportDisposition,
    GovernedDependencyVersionEvidence,
    UnsupportedDependencyResolutionError,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import PresentationAuthority
from bounded_product_ref.contract import build_p4_08_product_contract


UTC = timezone.utc


class P505IntegrationScaffoldingLocalHarnessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "p5-05-developer", "platform"))
        self.actor = ActorContext(self.principal, self.org)
        self.contract = build_p4_08_product_contract(
            actor=self.actor,
            created_at=datetime(2026, 8, 9, 14, 0, tzinfo=UTC),
        )

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

    def test_template_is_explicitly_provisional_and_compiles(self) -> None:
        template = render_integration_entry_template(module_name="product_integration")

        self.assertTrue(template.provisional)
        self.assertEqual(template.module_name, "product_integration")
        compile(template.source, "<p5.05-template>", "exec")
        self.assertIn("internal/provisional", template.source.lower())
        self.assertIn("stable/public", template.source.lower())

    def test_template_has_one_platform_import_boundary(self) -> None:
        template = render_integration_entry_template()
        tree = ast.parse(template.source)
        imports = tuple(
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
            and node.module is not None
            and node.module.startswith("arvectum_os_ref")
        )
        self.assertEqual(imports, ("arvectum_os_ref.integration_composition",))

    def test_template_does_not_copy_contract_resolution_or_domain_implementation(self) -> None:
        source = render_integration_entry_template().source.lower()
        for forbidden in (
            "bounded_product_ref",
            "product_contract_resolution",
            "validate_product_contract_declaration",
            "resolve_product_contract_dependencies",
            "build_p4_08_product_contract",
            "fastapi",
            "grpc",
            "requests",
            "socket",
            "yaml",
            "json",
            "protobuf",
            "openapi",
        ):
            self.assertNotIn(forbidden, source)

    def test_invalid_template_module_name_fails_closed(self) -> None:
        with self.assertRaises(ValueError):
            render_integration_entry_template(module_name="not-a-module")

    def test_local_harness_composes_exact_facade_and_non_authoritative_workspace(self) -> None:
        result = run_local_integration_harness(
            contract=self.contract,
            actor=self.actor,
            effective_product_contract=self.contract.version_pin,
            governed_versions=self._supported_versions(),
        )

        self.assertTrue(result.provisional)
        self.assertEqual(result.product_contract, self.contract.version_pin)
        self.assertEqual(result.facade.context.product_contract, self.contract.version_pin)
        self.assertEqual(result.workspace.presentation_authority, PresentationAuthority.NON_AUTHORITATIVE)
        self.assertIsNotNone(result.workspace.product_context)
        self.assertEqual(
            result.workspace.product_context.product_contract_version_id,
            self.contract.version_pin.version_id,
        )

    def test_local_harness_fails_closed_when_governed_dependency_evidence_is_missing(self) -> None:
        with self.assertRaises(UnsupportedDependencyResolutionError):
            run_local_integration_harness(
                contract=self.contract,
                actor=self.actor,
                effective_product_contract=self.contract.version_pin,
                governed_versions=self._supported_versions()[1:],
            )

    def test_local_harness_evidence_contains_no_authority_or_readiness_decision_fields(self) -> None:
        result = run_local_integration_harness(
            contract=self.contract,
            actor=self.actor,
            effective_product_contract=self.contract.version_pin,
            governed_versions=self._supported_versions(),
        )
        field_names = {item.name for item in fields(result)}
        for forbidden in (
            "authorization",
            "organizational_authority",
            "approval",
            "permission",
            "capability_lifecycle",
            "operational_readiness",
            "production",
        ):
            self.assertNotIn(forbidden, field_names)

    def test_scaffolding_module_remains_domain_neutral_and_infrastructure_free(self) -> None:
        source = inspect.getsource(scaffolding_module).lower()
        self.assertIn("internal/provisional", source)
        self.assertIn("compose_integration_facade", source)
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
            "subprocess",
        ):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
