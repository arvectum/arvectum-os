from __future__ import annotations

import ast
from dataclasses import fields, replace
from datetime import datetime, timezone
import inspect
import unittest

import arvectum_os_ref.external_consumer_onboarding as onboarding_module
from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.external_consumer_onboarding import (
    ExternalConsumerOnboardingError,
    ExternalConsumerRelianceState,
    ExternalConsumerRelianceStateError,
    disable_external_consumer,
    onboard_external_consumer,
    remove_external_consumer,
    require_external_consumer_enabled,
    upgrade_external_consumer,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_004_AUDIT_RECONSTRUCTION,
    CAPABILITY_CONTRACT_VERSION,
    OP_RECONSTRUCT_EXECUTION,
    CapabilityConsumptionRequest,
)
from arvectum_os_ref.product_contract import ProductBoundaryMechanism, ProductContractLifecycle
from arvectum_os_ref.product_contract_resolution import (
    DependencySupportDisposition,
    GovernedDependencyVersionEvidence,
    IncompatibleDependencyVersionError,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import OperationSideEffectClass
from external_creative_ref.contract import (
    EXTENSION_ID_VALUE,
    EXTENSION_VERSION,
    PRODUCT_CONTRACT_VERSION_VALUE,
    build_p8_06_product_contract,
    extension_id_for,
)
from external_creative_ref.onboarding import (
    SOURCE_COMMIT_SHA,
    SOURCE_DECLARATION_BLOB_SHA,
    SOURCE_DECLARATION_FORMAT_OWNER,
    SOURCE_DECLARATION_PATH,
    SOURCE_REPOSITORY,
    build_external_source_evidence,
)


UTC = timezone.utc
PROVIDER_GOVERNANCE_REFERENCE = (
    "docs/contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md:CAP-004:1.0.0"
)


class P806ExternalProductExtensionOnboardingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "arvectum", "platform"))
        self.principal = Principal(Identity("principal", "p8-06-owner", "platform"))
        self.actor = ActorContext(self.principal, self.organization)
        self.contract = build_p8_06_product_contract(
            actor=self.actor,
            created_at=datetime(2026, 8, 20, 18, 0, tzinfo=UTC),
        )
        self.source = build_external_source_evidence(
            organization=self.organization,
            actor=self.actor,
        )
        self.access = AccessRequest(
            actor=self.actor,
            purpose="creative-test-audit-reconstruction",
            required_right="read",
            allowed_classifications=("internal",),
        )
        self.request = CapabilityConsumptionRequest(
            organization=self.organization,
            product_id=extension_id_for(self.actor),
            product_version=EXTENSION_VERSION,
            dependency_id=CAP_004_AUDIT_RECONSTRUCTION,
            dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
            operation_name=OP_RECONSTRUCT_EXECUTION,
            access=self.access,
        )

    def _provider_evidence(
        self,
        *,
        version: str = CAPABILITY_CONTRACT_VERSION,
        disposition: DependencySupportDisposition = DependencySupportDisposition.SUPPORTED,
    ) -> tuple[GovernedDependencyVersionEvidence, ...]:
        kwargs = {}
        if disposition in (
            DependencySupportDisposition.DEPRECATED,
            DependencySupportDisposition.RETIRED,
        ):
            kwargs["migration_obligation"] = "Publish and review a new immutable Product Contract version."
        return (
            GovernedDependencyVersionEvidence(
                dependency_id=CAP_004_AUDIT_RECONSTRUCTION,
                contract_version=version,
                disposition=disposition,
                governance_reference=PROVIDER_GOVERNANCE_REFERENCE,
                **kwargs,
            ),
        )

    def _onboard(self, **overrides):
        contract = overrides.get("contract", self.contract)
        return onboard_external_consumer(
            source=overrides.get("source", self.source),
            contract=contract,
            request=overrides.get("request", self.request),
            effective_product_contract=overrides.get(
                "effective_product_contract",
                contract.version_pin,
            ),
            governed_versions=overrides.get("governed_versions", self._provider_evidence()),
        )

    def test_real_external_consumer_source_is_pinned_to_merged_repository_revision(self) -> None:
        self.assertEqual(SOURCE_REPOSITORY, "arvectum/creative-test-agent")
        self.assertEqual(SOURCE_COMMIT_SHA, "8dd5aab83beb29be10629f06a2c4e3255e51f06c")
        self.assertEqual(SOURCE_DECLARATION_PATH, "integrations/arvectum_os_p8_06_onboarding.json")
        self.assertEqual(SOURCE_DECLARATION_BLOB_SHA, "67d6e4cfe5f32577c82a3f35aff3c33fe2f71fd3")
        self.assertEqual(SOURCE_DECLARATION_FORMAT_OWNER, "arvectum/creative-test-agent")
        self.assertNotEqual(SOURCE_REPOSITORY, "arvectum/arvectum-os")
        self.assertNotEqual(self.source.declaration_format_owner, "arvectum/arvectum-os")
        self.assertFalse(self.source.enabled_by_default)

    def test_provisional_product_contract_matches_exact_external_identity_and_keeps_product_semantics_owned(self) -> None:
        self.assertEqual(self.contract.lifecycle, ProductContractLifecycle.PROVISIONAL)
        self.assertEqual(self.contract.product_id.namespace, "extension")
        self.assertEqual(self.contract.product_id.value, EXTENSION_ID_VALUE)
        self.assertEqual(self.contract.product_id.scope, "arvectum")
        self.assertEqual(self.contract.product_version, EXTENSION_VERSION)
        self.assertEqual(self.contract.record.version_id.value, PRODUCT_CONTRACT_VERSION_VALUE)
        self.assertEqual(tuple(item.dependency_id for item in self.contract.dependencies), (CAP_004_AUDIT_RECONSTRUCTION,))
        self.assertTrue(
            all(
                item.side_effect_classes == (OperationSideEffectClass.READ_ONLY,)
                for item in self.contract.operations
            )
        )
        self.assertTrue(all(not item.canonical_accesses for item in self.contract.operations))
        self.assertIn("Creative inputs, scoring, workflows", self.contract.bounded_scope)
        self.assertIn("creative-test workflows and approvals", self.source.product_owned_semantics)

    def test_onboarding_resolves_exact_product_contract_provider_version_and_operation(self) -> None:
        receipt = self._onboard()

        self.assertEqual(receipt.state, ExternalConsumerRelianceState.ONBOARDED)
        self.assertEqual(receipt.repository, SOURCE_REPOSITORY)
        self.assertEqual(receipt.source_commit_sha, SOURCE_COMMIT_SHA)
        self.assertEqual(receipt.declaration_blob_sha, SOURCE_DECLARATION_BLOB_SHA)
        self.assertEqual(receipt.consumer_id, self.contract.product_id)
        self.assertEqual(receipt.consumer_version, EXTENSION_VERSION)
        self.assertEqual(receipt.organization, self.organization)
        self.assertEqual(receipt.product_contract, self.contract.version_pin)
        self.assertEqual(receipt.dependency_id, CAP_004_AUDIT_RECONSTRUCTION)
        self.assertEqual(receipt.dependency_contract_version, CAPABILITY_CONTRACT_VERSION)
        self.assertEqual(receipt.operation_name, OP_RECONSTRUCT_EXECUTION)
        self.assertEqual(receipt.provider_governance_reference, PROVIDER_GOVERNANCE_REFERENCE)

    def test_nearby_provider_version_is_not_inferred_compatible(self) -> None:
        with self.assertRaises(IncompatibleDependencyVersionError):
            self._onboard(governed_versions=self._provider_evidence(version="1.0.1"))

    def test_undeclared_dependency_is_rejected_before_reliance(self) -> None:
        changed = replace(self.request, dependency_id=CAP_001_DOCUMENT_ARTIFACT)
        with self.assertRaises(ExternalConsumerOnboardingError):
            self._onboard(request=changed)

    def test_undeclared_operation_is_rejected_before_reliance(self) -> None:
        changed = replace(self.request, operation_name="p8.06.undeclared-operation")
        with self.assertRaises(ExternalConsumerOnboardingError):
            self._onboard(request=changed)

    def test_cross_organization_onboarding_is_rejected(self) -> None:
        foreign_organization = OrganizationScope(Identity("organization", "other-org", "platform"))
        foreign_actor = ActorContext(
            Principal(Identity("principal", "foreign-owner", "platform")),
            foreign_organization,
        )
        foreign_source = build_external_source_evidence(
            organization=foreign_organization,
            actor=foreign_actor,
        )
        foreign_access = AccessRequest(
            actor=foreign_actor,
            purpose=self.source.purpose,
            required_right="read",
            allowed_classifications=("internal",),
        )
        foreign_request = replace(
            self.request,
            organization=foreign_organization,
            product_id=foreign_source.consumer_id,
            access=foreign_access,
        )

        with self.assertRaises(ExternalConsumerOnboardingError):
            self._onboard(source=foreign_source, request=foreign_request)

    def test_least_privilege_must_match_external_declaration_exactly(self) -> None:
        excessive = replace(self.source, required_rights=("read", "export"))
        with self.assertRaises(ExternalConsumerOnboardingError):
            self._onboard(source=excessive)

        changed_access = replace(self.access, allowed_classifications=("internal", "restricted"))
        changed_request = replace(self.request, access=changed_access)
        with self.assertRaises(ExternalConsumerOnboardingError):
            self._onboard(request=changed_request)

    def test_private_coupling_and_hidden_shared_mutable_state_are_rejected(self) -> None:
        for mechanism in (
            ProductBoundaryMechanism.INTERNAL_TABLE,
            ProductBoundaryMechanism.INTERNAL_IMPORT,
            ProductBoundaryMechanism.UNDOCUMENTED_ENDPOINT,
            ProductBoundaryMechanism.PRIVATE_EVENT_STREAM,
            ProductBoundaryMechanism.IMPLICIT_SHARED_STATE,
        ):
            with self.subTest(mechanism=mechanism.value):
                with self.assertRaises(ExternalConsumerOnboardingError):
                    self._onboard(source=replace(self.source, boundary_mechanisms=(mechanism,)))

        with self.assertRaises(ExternalConsumerOnboardingError):
            self._onboard(source=replace(self.source, shared_mutable_state=True))

    def test_installing_declaration_does_not_enable_reliance_or_grant_authority(self) -> None:
        with self.assertRaises(ExternalConsumerOnboardingError):
            self._onboard(source=replace(self.source, enabled_by_default=True))

        receipt_fields = {item.name for item in fields(self._onboard())}
        for forbidden in (
            "authentication",
            "authorization",
            "permission",
            "organizational_authority",
            "approval",
            "capability_lifecycle",
            "active",
            "lifecycle",
        ):
            self.assertNotIn(forbidden, receipt_fields)

    def test_disable_and_remove_are_explicit_reversible_reliance_transitions(self) -> None:
        onboarded = self._onboard()
        disabled = disable_external_consumer(onboarded, reason="operator-disabled-optional-extension")
        self.assertEqual(disabled.state, ExternalConsumerRelianceState.DISABLED)
        with self.assertRaises(ExternalConsumerRelianceStateError):
            require_external_consumer_enabled(disabled)

        removed = remove_external_consumer(disabled, reason="integration-removed")
        self.assertEqual(removed.state, ExternalConsumerRelianceState.REMOVED)
        with self.assertRaises(ExternalConsumerRelianceStateError):
            require_external_consumer_enabled(removed)
        with self.assertRaises(ExternalConsumerRelianceStateError):
            remove_external_consumer(onboarded, reason="must-disable-first")

    def test_upgrade_requires_new_source_and_product_contract_versions_then_reresolves(self) -> None:
        previous = self._onboard()
        new_record = replace(
            self.contract.record,
            version_id=Identity(
                "product-contract-version",
                "creative-test-agent-audit-reconstruction-pc-v0.2.0",
                "arvectum",
            ),
        )
        new_contract = replace(
            self.contract,
            record=new_record,
            product_version="0.2.0",
        )
        new_source = replace(
            self.source,
            commit_sha="a" * 40,
            declaration_blob_sha="b" * 40,
            consumer_version="0.2.0",
        )
        new_request = replace(self.request, product_version="0.2.0")

        upgraded = upgrade_external_consumer(
            previous=previous,
            source=new_source,
            contract=new_contract,
            request=new_request,
            effective_product_contract=new_contract.version_pin,
            governed_versions=self._provider_evidence(),
        )
        self.assertEqual(upgraded.state, ExternalConsumerRelianceState.ONBOARDED)
        self.assertEqual(upgraded.consumer_version, "0.2.0")
        self.assertEqual(upgraded.source_commit_sha, "a" * 40)
        self.assertEqual(upgraded.product_contract, new_contract.version_pin)

        with self.assertRaises(ExternalConsumerRelianceStateError):
            upgrade_external_consumer(
                previous=previous,
                source=replace(new_source, consumer_version=EXTENSION_VERSION),
                contract=new_contract,
                request=new_request,
                effective_product_contract=new_contract.version_pin,
                governed_versions=self._provider_evidence(),
            )

    def test_external_onboarding_layer_remains_internal_static_and_not_a_registry_protocol(self) -> None:
        tree = ast.parse(inspect.getsource(onboarding_module))
        imported_roots = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])
        for forbidden in ("requests", "httpx", "urllib", "socket", "packaging", "semver"):
            self.assertNotIn(forbidden, imported_roots)

        source = inspect.getsource(onboarding_module).lower()
        self.assertIn("internal reference slice", source)
        self.assertIn("not define a public sdk/api", source)
        self.assertIn("not a platform manifest", source)
        self.assertIn("not a governed lifecycle model", source)
        self.assertNotIn("auto-fallback", source)


if __name__ == "__main__":
    unittest.main()
