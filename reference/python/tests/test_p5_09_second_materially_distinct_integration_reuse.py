from __future__ import annotations

import ast
from dataclasses import replace
from datetime import datetime, timezone
import inspect
import unittest

import bounded_product_ref.integration_adapter_journey as first_journey
import evidence_extension_ref.reconstruction_journey as second_journey
from arvectum_os_ref.audit_reconstruction_support import EvidenceAvailability
from arvectum_os_ref.cross_capability_enforcement import (
    AccessRequest,
    CrossCapabilityEnforcementError,
)
from arvectum_os_ref.event_provenance import ReconstructionManifest
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.integration_adapters import compose_integration_adapters
from arvectum_os_ref.integration_composition import IntegrationCompositionEvidenceRequiredError
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_002_MEMORY_KNOWLEDGE,
    CAP_004_AUDIT_RECONSTRUCTION,
    CAPABILITY_CONTRACT_VERSION,
    OP_RECONSTRUCT_EXECUTION,
    CapabilityConsumptionRequest,
)
from arvectum_os_ref.product_contract import ProductContractLifecycle
from arvectum_os_ref.product_contract_declaration import validate_product_contract_declaration
from arvectum_os_ref.product_contract_resolution import (
    DependencySupportDisposition,
    GovernedDependencyVersionEvidence,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import OperationSideEffectClass
from bounded_product_ref.contract import (
    GOVERNED_RUNTIME_DEPENDENCY,
    build_p4_08_product_contract,
)
from evidence_extension_ref.contract import (
    EXTENSION_VERSION,
    build_p5_09_product_contract,
    extension_id_for,
)
from evidence_extension_ref.reconstruction_journey import inspect_execution_evidence


UTC = timezone.utc


class P509SecondMateriallyDistinctIntegrationReuseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "p5-09-evidence-reviewer", "platform"))
        self.actor = ActorContext(self.principal, self.org)
        self.extension_id = extension_id_for(self.actor)
        self.contract = build_p5_09_product_contract(
            actor=self.actor,
            created_at=datetime(2026, 8, 9, 16, 0, tzinfo=UTC),
        )
        self.access = AccessRequest(
            actor=self.actor,
            purpose="governed-evidence-review",
            required_right="read",
            allowed_classifications=("internal",),
        )
        self.request = CapabilityConsumptionRequest(
            organization=self.org,
            product_id=self.extension_id,
            product_version=EXTENSION_VERSION,
            dependency_id=CAP_004_AUDIT_RECONSTRUCTION,
            dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
            operation_name=OP_RECONSTRUCT_EXECUTION,
            access=self.access,
        )

    def _supported_versions(self) -> tuple[GovernedDependencyVersionEvidence, ...]:
        return (
            GovernedDependencyVersionEvidence(
                dependency_id=CAP_004_AUDIT_RECONSTRUCTION,
                contract_version=CAPABILITY_CONTRACT_VERSION,
                disposition=DependencySupportDisposition.SUPPORTED,
                governance_reference="p5.09-current-cap004-provider-evidence",
            ),
        )

    def _adapters(self):
        return compose_integration_adapters(
            contract=self.contract,
            actor=self.actor,
            effective_product_contract=self.contract.version_pin,
            governed_versions=self._supported_versions(),
        )

    def _id(self, namespace: str, value: str, scope: str = "org-a") -> Identity:
        return Identity(namespace, value, scope)

    def _pin(self, role: str, *, scope: str = "org-a") -> GovernedVersionPin:
        return GovernedVersionPin(
            self._id(f"{role}-subject", role, scope),
            self._id(f"{role}-version", f"{role}-v1", scope),
            f"example.{role}",
            f"{role}/state",
            "Retained",
        )

    def _manifest(self, *, scope: str = "org-a"):
        organization = OrganizationScope(Identity("organization", scope, "platform"))
        workflow, material, source_contract, execution, result, event = (
            self._pin(role, scope=scope)
            for role in (
                "workflow",
                "material",
                "source-product-contract",
                "execution",
                "result",
                "event",
            )
        )
        execution_subject = self._id("execution-subject", "reviewed-execution", scope)
        manifest = ReconstructionManifest(
            organization=organization,
            execution_subject_id=execution_subject,
            initiating_actor_id=self.principal.principal_id,
            operation_name="source-product.consequential-operation",
            workflow=workflow,
            material_inputs=(material,),
            product_contract=source_contract,
            gate_decisions=(),
            execution_versions=(execution,),
            results=(result,),
            events=(event,),
            event_types=(("source-product.event", "1"),),
            correlation_refs=(execution_subject,),
            causation_refs=(execution.version_id,),
            provenance_refs=(
                self.principal.principal_id,
                execution_subject,
                workflow.subject_id,
                workflow.version_id,
                material.subject_id,
                material.version_id,
                source_contract.subject_id,
                source_contract.version_id,
                execution.subject_id,
                execution.version_id,
                result.subject_id,
                result.version_id,
                event.subject_id,
                event.version_id,
            ),
        )
        pins = (workflow, material, source_contract, execution, result, event)
        constraints = tuple(
            (pin.version_id, "governed-evidence-review", ("read",), "internal")
            for pin in pins
        )
        return manifest, constraints

    def test_second_contract_is_materially_distinct_from_first_product_contract(self) -> None:
        first = build_p4_08_product_contract(
            actor=self.actor,
            created_at=datetime(2026, 8, 9, 15, 0, tzinfo=UTC),
        )

        self.assertNotEqual(first.product_id, self.contract.product_id)
        self.assertEqual(self.contract.product_id.namespace, "extension")
        self.assertEqual(self.contract.lifecycle, ProductContractLifecycle.PROVISIONAL)
        self.assertEqual(
            tuple(item.dependency_id for item in self.contract.dependencies),
            (CAP_004_AUDIT_RECONSTRUCTION,),
        )
        first_dependencies = {item.dependency_id for item in first.dependencies}
        self.assertIn(CAP_001_DOCUMENT_ARTIFACT, first_dependencies)
        self.assertIn(CAP_002_MEMORY_KNOWLEDGE, first_dependencies)
        self.assertIn(GOVERNED_RUNTIME_DEPENDENCY, first_dependencies)
        self.assertNotIn(CAP_004_AUDIT_RECONSTRUCTION, first_dependencies)
        self.assertTrue(
            any(
                OperationSideEffectClass.CANONICAL_MUTATION in item.side_effect_classes
                for item in first.operations
            )
        )
        self.assertTrue(
            all(item.side_effect_classes == (OperationSideEffectClass.READ_ONLY,) for item in self.contract.operations)
        )
        self.assertTrue(all(not item.canonical_accesses for item in self.contract.operations))

    def test_second_contract_reuses_p5_02_declaration_validation_without_fake_canonical_read(self) -> None:
        validation = validate_product_contract_declaration(contract=self.contract)

        self.assertEqual(validation.product_contract, self.contract.version_pin)
        self.assertEqual(validation.product_id, self.extension_id)
        self.assertEqual(len(validation.dependencies), 1)
        self.assertEqual(validation.dependencies[0].dependency_id, CAP_004_AUDIT_RECONSTRUCTION)
        self.assertEqual(validation.canonical_accesses, ())

    def test_both_consumers_use_the_same_integration_adapter_module(self) -> None:
        def platform_imports(module) -> tuple[str, ...]:
            tree = ast.parse(inspect.getsource(module))
            return tuple(
                node.module
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom)
                and node.module is not None
                and node.module.startswith("arvectum_os_ref")
            )

        self.assertEqual(platform_imports(first_journey), ("arvectum_os_ref.integration_adapters",))
        self.assertEqual(platform_imports(second_journey), ("arvectum_os_ref.integration_adapters",))

    def test_second_consumer_has_no_workspace_event_store_or_capability_private_import(self) -> None:
        source = inspect.getsource(second_journey).lower()
        for forbidden in (
            "workspace_shell",
            "audit_reconstruction_support",
            "event_provenance",
            "cross_capability_enforcement",
            "product_capability_consumption",
            "canonical",
            "governed_execution",
            "search_index_projection",
            "memory_knowledge_governance",
            "document_artifact_governance",
        ):
            self.assertNotIn(forbidden, source)
        self.assertNotIn("open_workspace", source)
        self.assertNotIn("navigate_workspace", source)
        self.assertNotIn("start_governed_execution", source)

    def test_reconstruction_executes_through_same_adapters_and_preserves_exact_contract_context(self) -> None:
        manifest, constraints = self._manifest()
        adapters = self._adapters()

        entry = inspect_execution_evidence(
            adapters=adapters,
            request=self.request,
            governed_versions=self._supported_versions(),
            manifest=manifest,
            evidence_constraints=constraints,
        )

        self.assertEqual(entry.inspection_mode, "read-only-governed-evidence")
        self.assertTrue(entry.reconstruction.complete)
        self.assertEqual(entry.reconstruction.organization, self.org)
        self.assertEqual(entry.reconstruction.execution_subject_id, manifest.execution_subject_id)
        self.assertEqual(
            adapters.facade.context.product_contract,
            self.contract.version_pin,
        )
        self.assertEqual(len(entry.reconstruction.evidence), 6)

    def test_evidence_rights_remain_owned_by_capability_and_redact_without_private_fallback(self) -> None:
        manifest, constraints = self._manifest()
        denied_version = constraints[-1][0]
        restricted = constraints[:-1] + (
            (denied_version, "governed-evidence-review", ("different-right",), "internal"),
        )

        entry = inspect_execution_evidence(
            adapters=self._adapters(),
            request=self.request,
            governed_versions=self._supported_versions(),
            manifest=manifest,
            evidence_constraints=restricted,
        )

        self.assertFalse(entry.reconstruction.complete)
        denied = tuple(item for item in entry.reconstruction.evidence if item.version_id == denied_version)
        self.assertEqual(len(denied), 1)
        self.assertEqual(denied[0].availability, EvidenceAvailability.REDACTED)
        self.assertIsNone(denied[0].source)
        self.assertIsNotNone(denied[0].reason)

    def test_cross_organization_reconstruction_fails_closed(self) -> None:
        foreign_manifest, foreign_constraints = self._manifest(scope="org-b")

        with self.assertRaises(CrossCapabilityEnforcementError):
            inspect_execution_evidence(
                adapters=self._adapters(),
                request=self.request,
                governed_versions=self._supported_versions(),
                manifest=foreign_manifest,
                evidence_constraints=foreign_constraints,
            )

    def test_current_provider_evidence_is_still_required_for_second_integration(self) -> None:
        manifest, constraints = self._manifest()

        with self.assertRaises(IntegrationCompositionEvidenceRequiredError):
            inspect_execution_evidence(
                adapters=self._adapters(),
                request=self.request,
                governed_versions=None,
                manifest=manifest,
                evidence_constraints=constraints,
            )

    def test_second_integration_cannot_smuggle_an_undeclared_dependency(self) -> None:
        changed_request = replace(
            self.request,
            dependency_id=CAP_001_DOCUMENT_ARTIFACT,
        )
        manifest, constraints = self._manifest()

        with self.assertRaises(Exception) as caught:
            inspect_execution_evidence(
                adapters=self._adapters(),
                request=changed_request,
                governed_versions=self._supported_versions(),
                manifest=manifest,
                evidence_constraints=constraints,
            )
        self.assertNotIsInstance(caught.exception, CrossCapabilityEnforcementError)

    def test_reuse_does_not_promote_capability_or_contract_lifecycle(self) -> None:
        self.assertEqual(self.contract.lifecycle, ProductContractLifecycle.PROVISIONAL)
        self.assertTrue(self.contract.dependencies[0].provisional)
        self.assertFalse(
            any(
                OperationSideEffectClass.CANONICAL_MUTATION in operation.side_effect_classes
                for operation in self.contract.operations
            )
        )


if __name__ == "__main__":
    unittest.main()
