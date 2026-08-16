from __future__ import annotations

import ast
from dataclasses import replace
import inspect
import unittest

from arvectum_os_ref.integration_composition import IntegrationCompositionEvidenceRequiredError
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_002_MEMORY_KNOWLEDGE,
    CAP_003_SEARCH_PROJECTION,
    CAP_004_AUDIT_RECONSTRUCTION,
)
from arvectum_os_ref.product_contract import ProductContractLifecycle
from arvectum_os_ref.workflow import OperationSideEffectClass
import p6_07_discount_parser_ref.journey as product_journey
from p6_07_discount_parser_ref.contract import (
    P6_06_CANONICAL_BLOB_SHA,
    P6_06_CANONICAL_CONTRACT_PATH,
    PRODUCT_COMPATIBILITY_LINE,
    PRODUCT_CONTRACT_VERSION,
)
from p6_07_discount_parser_ref.journey import (
    P607IntegrationContinuityError,
    reconstruct_publication,
)
from p6_07_discount_parser_ref.scenario import (
    CLASSIFICATION,
    PURPOSE,
    FakeTelegramAdapter,
    P607Stage1Error,
    PublicationOutcome,
    build_stage1_scenario,
    execute_stage1_publication,
)


class P607SecondRealProductWorkflowIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scenario = build_stage1_scenario()

    def _constraints_from_complete_view(self, view):
        return tuple(
            (item.version_id, PURPOSE, ("read",), CLASSIFICATION)
            for item in view.evidence
        )

    def test_exact_p6_06_contract_and_cap004_only_dependency_are_preserved(self) -> None:
        contract = self.scenario.contract
        self.assertEqual(contract.lifecycle, ProductContractLifecycle.PROVISIONAL)
        self.assertEqual(PRODUCT_CONTRACT_VERSION, "0.1.0")
        self.assertEqual(contract.product_version, PRODUCT_COMPATIBILITY_LINE)
        self.assertEqual(contract.record.version_id.value, "p6-06-arvectum-discount-parser-v0.1.0")
        self.assertEqual(
            dict(contract.record.payload)["canonical_contract"],
            P6_06_CANONICAL_CONTRACT_PATH,
        )
        self.assertEqual(
            dict(contract.record.payload)["canonical_blob_sha"],
            P6_06_CANONICAL_BLOB_SHA,
        )

        dependency_ids = {item.dependency_id for item in contract.dependencies}
        self.assertEqual(dependency_ids, {CAP_004_AUDIT_RECONSTRUCTION})
        self.assertNotIn(CAP_001_DOCUMENT_ARTIFACT, dependency_ids)
        self.assertNotIn(CAP_002_MEMORY_KNOWLEDGE, dependency_ids)
        self.assertNotIn(CAP_003_SEARCH_PROJECTION, dependency_ids)
        self.assertTrue(all(item.provisional for item in contract.dependencies))
        self.assertTrue(
            all(
                item.side_effect_classes == (OperationSideEffectClass.READ_ONLY,)
                and not item.canonical_accesses
                for item in contract.operations
            )
        )

    def test_published_offline_attempt_reconstructs_exact_minimized_evidence(self) -> None:
        telegram = FakeTelegramAdapter(PublicationOutcome.PUBLISHED)
        result = execute_stage1_publication(self.scenario, telegram=telegram)

        self.assertEqual(result.outcome, PublicationOutcome.PUBLISHED)
        self.assertEqual(result.telegram_send_calls, 1)
        self.assertIsNotNone(result.telegram_message)
        self.assertTrue(result.reconstruction.complete)
        self.assertEqual(result.reconstruction.organization, self.scenario.organization)
        self.assertEqual(
            result.manifest.product_contract,
            self.scenario.contract.version_pin,
        )
        self.assertEqual(
            self.scenario.adapters.facade.context.product_contract,
            self.scenario.contract.version_pin,
        )

        evidence_versions = {item.version_id for item in result.reconstruction.evidence}
        required_product_refs = {
            self.scenario.refs.parse_run.version_id,
            self.scenario.refs.source_observation.version_id,
            self.scenario.refs.offer.version_id,
            self.scenario.refs.publication_candidate.version_id,
            self.scenario.refs.rule_config.version_id,
            self.scenario.refs.template_version.version_id,
            self.scenario.refs.publication_reservation.version_id,
            self.scenario.refs.publication_attempt.version_id,
            self.scenario.refs.telegram_target.version_id,
            self.scenario.contract.version_pin.version_id,
            result.telegram_message.version_id,
        }
        self.assertTrue(required_product_refs.issubset(evidence_versions))

    def test_missing_pre_effect_evidence_fails_before_external_call(self) -> None:
        telegram = FakeTelegramAdapter(PublicationOutcome.PUBLISHED)
        with self.assertRaises(P607Stage1Error):
            execute_stage1_publication(
                self.scenario,
                telegram=telegram,
                pre_effect_evidence_available=False,
            )
        self.assertEqual(telegram.send_calls, 0)

    def test_known_duplicate_is_not_sent_and_remains_reconstructable(self) -> None:
        telegram = FakeTelegramAdapter(PublicationOutcome.PUBLISHED)
        result = execute_stage1_publication(
            self.scenario,
            telegram=telegram,
            duplicate_reserved=True,
        )
        self.assertEqual(result.outcome, PublicationOutcome.DUPLICATE_NOT_APPLICABLE)
        self.assertEqual(result.telegram_send_calls, 0)
        self.assertIsNone(result.telegram_message)
        self.assertTrue(result.reconstruction.complete)

    def test_ambiguous_external_outcome_is_reconciliation_required_without_blind_retry(self) -> None:
        telegram = FakeTelegramAdapter(PublicationOutcome.UNCERTAIN_RECONCILIATION_REQUIRED)
        result = execute_stage1_publication(self.scenario, telegram=telegram)
        self.assertEqual(
            result.outcome,
            PublicationOutcome.UNCERTAIN_RECONCILIATION_REQUIRED,
        )
        self.assertEqual(result.telegram_send_calls, 1)
        self.assertIsNone(result.telegram_message)
        self.assertTrue(result.reconstruction.complete)
        self.assertIn("uncertain/reconciliation-required", result.manifest.results[0].subject_id.value)

    def test_missing_product_contract_version_pin_fails_closed(self) -> None:
        result = execute_stage1_publication(
            self.scenario,
            telegram=FakeTelegramAdapter(PublicationOutcome.PUBLISHED),
        )
        missing_contract = replace(result.manifest, product_contract=None)
        with self.assertRaises(P607IntegrationContinuityError):
            reconstruct_publication(
                adapters=self.scenario.adapters,
                request=self.scenario.reconstruction_request,
                governed_versions=self.scenario.governed_versions,
                manifest=missing_contract,
                evidence_constraints=self._constraints_from_complete_view(result.reconstruction),
            )

    def test_wrong_organization_evidence_fails_closed_at_product_boundary(self) -> None:
        foreign = build_stage1_scenario(scope="p6-07-org-b")
        foreign_result = execute_stage1_publication(
            foreign,
            telegram=FakeTelegramAdapter(PublicationOutcome.PUBLISHED),
        )
        with self.assertRaises(P607IntegrationContinuityError):
            reconstruct_publication(
                adapters=self.scenario.adapters,
                request=foreign.reconstruction_request,
                governed_versions=self.scenario.governed_versions,
                manifest=foreign_result.manifest,
                evidence_constraints=self._constraints_from_complete_view(foreign_result.reconstruction),
            )

    def test_current_cap004_provider_evidence_cannot_be_omitted(self) -> None:
        result = execute_stage1_publication(
            self.scenario,
            telegram=FakeTelegramAdapter(PublicationOutcome.PUBLISHED),
        )
        with self.assertRaises(IntegrationCompositionEvidenceRequiredError):
            reconstruct_publication(
                adapters=self.scenario.adapters,
                request=self.scenario.reconstruction_request,
                governed_versions=None,
                manifest=result.manifest,
                evidence_constraints=self._constraints_from_complete_view(result.reconstruction),
            )

    def test_product_journey_uses_only_shared_integration_adapter_surface(self) -> None:
        tree = ast.parse(inspect.getsource(product_journey))
        platform_imports = tuple(
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
            and node.module is not None
            and node.module.startswith("arvectum_os_ref")
        )
        self.assertEqual(platform_imports, ("arvectum_os_ref.integration_adapters",))

        source = inspect.getsource(product_journey).lower()
        for forbidden in (
            "internal_table",
            "private_event_stream",
            "workspace_shell",
            "audit_reconstruction_support",
            "event_provenance",
            "canonicalrecord",
            "offer",
            "telegram",
        ):
            self.assertNotIn(forbidden, source)

    def test_stage1_fixture_contains_no_live_network_or_secret_dependency(self) -> None:
        import p6_07_discount_parser_ref.scenario as scenario_module

        source = inspect.getsource(scenario_module).lower()
        self.assertNotIn("requests", source)
        self.assertNotIn("httpx", source)
        self.assertNotIn("bot_token", source)
        self.assertNotIn("api_key", source)
        self.assertNotIn("private_key", source)


if __name__ == "__main__":
    unittest.main()
