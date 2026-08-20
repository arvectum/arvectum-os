from __future__ import annotations

from dataclasses import fields, replace
from datetime import datetime, timezone
from pathlib import Path
import unittest

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
    CAP_004_AUDIT_RECONSTRUCTION,
    CAPABILITY_CONTRACT_VERSION,
    OP_RECONSTRUCT_EXECUTION,
    CapabilityConsumptionRequest,
)
from arvectum_os_ref.product_contract_resolution import (
    DependencySupportDisposition,
    DeprecatedDependencyResolutionError,
    GovernedDependencyVersionEvidence,
    IncompatibleDependencyVersionError,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from external_creative_ref.contract import (
    EXTENSION_VERSION,
    PRODUCT_CONTRACT_VERSION_VALUE,
    build_p8_06_product_contract,
    extension_id_for,
)
from external_creative_ref.onboarding import (
    SOURCE_COMMIT_SHA,
    SOURCE_DECLARATION_BLOB_SHA,
    SOURCE_DECLARATION_PATH,
    SOURCE_REPOSITORY,
    build_external_source_evidence,
)


UTC = timezone.utc
PROVIDER_GOVERNANCE_REFERENCE = (
    "docs/contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md:CAP-004:1.0.0"
)
RUNBOOK_PATH = (
    Path(__file__).resolve().parents[3]
    / "docs"
    / "implementation"
    / "P8-09-EXTERNAL-OPERATOR-DEVELOPER-INTEGRATION-RUNBOOK.md"
)


class P809ExternalOperatorDeveloperExperienceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "arvectum", "platform"))
        self.actor = ActorContext(
            Principal(Identity("principal", "p8-09-operator", "platform")),
            self.organization,
        )
        self.contract = build_p8_06_product_contract(
            actor=self.actor,
            created_at=datetime(2026, 8, 20, 20, 0, tzinfo=UTC),
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
        migration_obligation = None
        if disposition in (
            DependencySupportDisposition.DEPRECATED,
            DependencySupportDisposition.RETIRED,
        ):
            migration_obligation = (
                "Publish and review a new immutable Product Contract version before renewed reliance."
            )
        return (
            GovernedDependencyVersionEvidence(
                dependency_id=CAP_004_AUDIT_RECONSTRUCTION,
                contract_version=version,
                disposition=disposition,
                governance_reference=PROVIDER_GOVERNANCE_REFERENCE,
                migration_obligation=migration_obligation,
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

    def test_runbook_pins_exact_validated_boundary_and_non_claims(self) -> None:
        runbook = RUNBOOK_PATH.read_text(encoding="utf-8")

        for exact_value in (
            SOURCE_REPOSITORY,
            SOURCE_COMMIT_SHA,
            SOURCE_DECLARATION_PATH,
            SOURCE_DECLARATION_BLOB_SHA,
            PRODUCT_CONTRACT_VERSION_VALUE,
            CAPABILITY_CONTRACT_VERSION,
            OP_RECONSTRUCT_EXECUTION,
            "creative-test-audit-reconstruction",
        ):
            self.assertIn(exact_value, runbook)

        for required_boundary in (
            "not a universal extension specification",
            "Public/stable surface: `NONE`",
            "must not import `arvectum_os_ref` private/reference modules as a supported public SDK contract",
            "multi-Organization isolation",
            "Configuration is not authority",
            "Onboarded → Disabled → Removed",
        ):
            self.assertIn(required_boundary, runbook)

    def test_documented_happy_path_reproduces_exact_point_in_time_receipt(self) -> None:
        receipt = self._onboard()

        self.assertEqual(receipt.state, ExternalConsumerRelianceState.ONBOARDED)
        self.assertEqual(receipt.repository, SOURCE_REPOSITORY)
        self.assertEqual(receipt.source_commit_sha, SOURCE_COMMIT_SHA)
        self.assertEqual(receipt.declaration_blob_sha, SOURCE_DECLARATION_BLOB_SHA)
        self.assertEqual(receipt.consumer_version, EXTENSION_VERSION)
        self.assertEqual(receipt.product_contract, self.contract.version_pin)
        self.assertEqual(receipt.dependency_id, CAP_004_AUDIT_RECONSTRUCTION)
        self.assertEqual(receipt.dependency_contract_version, CAPABILITY_CONTRACT_VERSION)
        self.assertEqual(receipt.operation_name, OP_RECONSTRUCT_EXECUTION)
        self.assertEqual(receipt.organization, self.organization)

    def test_documented_version_and_scope_drift_fail_closed(self) -> None:
        with self.assertRaises(IncompatibleDependencyVersionError):
            self._onboard(governed_versions=self._provider_evidence(version="1.0.1"))

        excessive_access = replace(self.access, allowed_classifications=("internal", "restricted"))
        with self.assertRaises(ExternalConsumerOnboardingError):
            self._onboard(request=replace(self.request, access=excessive_access))

        with self.assertRaises(DeprecatedDependencyResolutionError):
            self._onboard(
                governed_versions=self._provider_evidence(
                    disposition=DependencySupportDisposition.DEPRECATED
                )
            )

    def test_documented_disable_remove_and_upgrade_rules_are_enforced(self) -> None:
        onboarded = self._onboard()
        with self.assertRaises(ExternalConsumerRelianceStateError):
            remove_external_consumer(onboarded, reason="must-disable-first")

        disabled = disable_external_consumer(onboarded, reason="operator-stop")
        with self.assertRaises(ExternalConsumerRelianceStateError):
            require_external_consumer_enabled(disabled)

        removed = remove_external_consumer(disabled, reason="integration-terminated")
        self.assertEqual(removed.state, ExternalConsumerRelianceState.REMOVED)
        with self.assertRaises(ExternalConsumerRelianceStateError):
            require_external_consumer_enabled(removed)

        with self.assertRaises(ExternalConsumerRelianceStateError):
            upgrade_external_consumer(
                previous=onboarded,
                source=self.source,
                contract=self.contract,
                request=self.request,
                effective_product_contract=self.contract.version_pin,
                governed_versions=self._provider_evidence(),
            )

    def test_source_and_receipt_evidence_do_not_embed_reusable_secret_fields(self) -> None:
        receipt = self._onboard()
        evidence_field_names = {
            item.name.lower()
            for item in (*fields(self.source), *fields(receipt))
        }
        forbidden_fragments = ("password", "secret", "private_key", "credential", "access_token")

        for field_name in evidence_field_names:
            self.assertFalse(
                any(fragment in field_name for fragment in forbidden_fragments),
                field_name,
            )

        runbook = RUNBOOK_PATH.read_text(encoding="utf-8")
        self.assertIn("credentials must be separately reprovisioned", runbook)
        self.assertIn("never copy secrets into onboarding receipts", runbook)


if __name__ == "__main__":
    unittest.main()
