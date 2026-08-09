from __future__ import annotations

from dataclasses import fields, replace
from datetime import datetime, timezone
import inspect
import unittest

import arvectum_os_ref.integration_adapters as adapter_module
from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.integration_adapters import (
    IntegrationCapabilityAdapter,
    compose_integration_adapters,
)
from arvectum_os_ref.integration_composition import (
    IntegrationCompositionContinuityError,
    IntegrationCompositionEvidenceRequiredError,
)
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAPABILITY_CONTRACT_VERSION,
    OP_RESOLVE_DOCUMENT,
    CapabilityConsumptionRequest,
)
from arvectum_os_ref.product_contract_declaration import validate_product_contract_declaration
from arvectum_os_ref.product_contract_resolution import (
    DependencySupportDisposition,
    GovernedDependencyVersionEvidence,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from bounded_product_ref.contract import (
    PRODUCT_VERSION,
    build_p4_08_product_contract,
    product_id_for,
)
from evidence_extension_ref.contract import build_p5_09_product_contract


UTC = timezone.utc


class R16M5IntegrationHardeningTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "r16-reviewer", "platform"))
        self.actor = ActorContext(self.principal, self.org)
        self.product_contract = build_p4_08_product_contract(
            actor=self.actor,
            created_at=datetime(2026, 8, 9, 17, 30, tzinfo=UTC),
        )
        self.extension_contract = build_p5_09_product_contract(
            actor=self.actor,
            created_at=datetime(2026, 8, 9, 17, 35, tzinfo=UTC),
        )

    @staticmethod
    def _supported_versions(contract) -> tuple[GovernedDependencyVersionEvidence, ...]:
        return tuple(
            GovernedDependencyVersionEvidence(
                dependency_id=dependency.dependency_id,
                contract_version=dependency.contract_version,
                disposition=DependencySupportDisposition.SUPPORTED,
                governance_reference=(
                    "r16-current-provider-evidence:"
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

    def _document_request(self) -> CapabilityConsumptionRequest:
        access = AccessRequest(
            actor=self.actor,
            purpose="r16-integration-hardening",
            required_right="read",
            allowed_classifications=("internal",),
        )
        return CapabilityConsumptionRequest(
            organization=self.org,
            product_id=product_id_for(self.actor),
            product_version=PRODUCT_VERSION,
            dependency_id=CAP_001_DOCUMENT_ARTIFACT,
            dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
            operation_name=OP_RESOLVE_DOCUMENT,
            access=access,
        )

    def test_capability_adapter_is_bound_to_exact_facade_declaration_evidence(self) -> None:
        adapters = self._adapters(self.product_contract)

        self.assertEqual(
            validate_product_contract_declaration(contract=adapters.capabilities.contract),
            adapters.facade.declaration_evidence,
        )
        self.assertEqual(adapters.capabilities.contract.version_pin, adapters.facade.context.product_contract)

    def test_r16_f1_same_version_alternate_contract_semantics_fail_closed(self) -> None:
        adapters = self._adapters(self.product_contract)
        drifted = replace(
            self.product_contract,
            bounded_scope=self.product_contract.bounded_scope + " caller-added semantic drift",
        )

        self.assertEqual(drifted.version_pin, self.product_contract.version_pin)
        self.assertNotEqual(
            validate_product_contract_declaration(contract=drifted),
            adapters.facade.declaration_evidence,
        )
        with self.assertRaises(IntegrationCompositionContinuityError):
            IntegrationCapabilityAdapter(adapters.facade, drifted)

    def test_r16_f1_dependency_responsibility_drift_under_same_version_fails_closed(self) -> None:
        adapters = self._adapters(self.product_contract)
        dependency = self.product_contract.dependencies[0]
        drifted_dependency = replace(
            dependency,
            consumer_responsibility=dependency.consumer_responsibility + " altered by adapter caller",
        )
        drifted = replace(
            self.product_contract,
            dependencies=(drifted_dependency,) + self.product_contract.dependencies[1:],
        )

        self.assertEqual(drifted.version_pin, self.product_contract.version_pin)
        with self.assertRaises(IntegrationCompositionContinuityError):
            IntegrationCapabilityAdapter(adapters.facade, drifted)

    def test_two_materially_distinct_consumers_still_compose_through_hardened_adapter(self) -> None:
        product = self._adapters(self.product_contract)
        extension = self._adapters(self.extension_contract)

        self.assertEqual(
            validate_product_contract_declaration(contract=product.capabilities.contract),
            product.facade.declaration_evidence,
        )
        self.assertEqual(
            validate_product_contract_declaration(contract=extension.capabilities.contract),
            extension.facade.declaration_evidence,
        )
        self.assertIs(product.capabilities.facade, product.facade)
        self.assertIs(extension.capabilities.facade, extension.facade)

    def test_r14_current_provider_evidence_guard_remains_fail_closed_after_hardening(self) -> None:
        adapters = self._adapters(self.product_contract)

        with self.assertRaises(IntegrationCompositionEvidenceRequiredError):
            adapters.capabilities.admit(
                self._document_request(),
                governed_versions=None,
            )

    def test_hardening_does_not_add_authority_or_lifecycle_state_to_adapter(self) -> None:
        adapters = self._adapters(self.product_contract)
        field_names = {field.name for field in fields(adapters.capabilities)}

        self.assertEqual(field_names, {"facade", "contract"})
        for forbidden in (
            "authorization",
            "permission",
            "organizational_authority",
            "approval",
            "capability_lifecycle",
            "active",
        ):
            self.assertNotIn(forbidden, field_names)

    def test_hardening_remains_internal_provisional_and_uses_existing_semantic_owner(self) -> None:
        source = inspect.getsource(adapter_module).lower()

        self.assertIn("internal/provisional", source)
        self.assertIn("r16", source)
        self.assertIn("validate_product_contract_declaration", source)
        self.assertIn("facade.declaration_evidence", source)
        self.assertIn("not a new semantic owner", source)
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
