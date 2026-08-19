from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

import p7_09_operator_recovery_drills as p709


class P709OperatorRecoveryDrillTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        self.release_sha = "a" * 40

    def _common(self) -> dict:
        return {
            "operator_attributable": True,
            "organization_scope_verified": True,
            "reusable_secret_exposed": False,
            "canonical_mutation_by_drill": False,
            "external_effect_invoked_by_drill": False,
        }

    def _evaluate(self, scenario: str, **specific):
        return p709.evaluate(scenario, {**self._common(), **specific})

    def test_catalog_covers_all_required_phase7_scenarios(self) -> None:
        catalog = p709.catalog()
        self.assertEqual(list(catalog["scenarios"]), list(p709.SCENARIOS))
        self.assertEqual(len(catalog["scenarios"]), 9)
        for scenario in p709.SCENARIOS:
            self.assertTrue(catalog["scenarios"][scenario]["runbook_routes"])

    def test_runtime_crash_recovers_without_replay(self) -> None:
        value = self._evaluate(
            "runtime-crash",
            runtime_status_after="healthy",
            exact_release_verified=True,
            supervised_generation_advanced=True,
            historical_effect_replayed=False,
        )
        self.assertEqual(value["decision"], p709.PASS)
        self.assertFalse(value["historical_external_effect_replay_authorized"])
        self.assertFalse(value["consequential_action_authorized_by_drill"])

    def test_runtime_crash_with_replay_fails_closed(self) -> None:
        value = self._evaluate(
            "runtime-crash",
            runtime_status_after="healthy",
            exact_release_verified=True,
            supervised_generation_advanced=True,
            historical_effect_replayed=True,
        )
        self.assertEqual(value["decision"], p709.FAIL_CLOSED)
        self.assertTrue(value["new_effect_authorization_required"])

    def test_mac_restart_requires_runtime_observer_release_and_state_integrity(self) -> None:
        value = self._evaluate(
            "mac-restart",
            runtime_status_after="healthy",
            observer_loaded=True,
            exact_release_consistent=True,
            durable_state_integrity_verified=True,
            historical_effect_replayed=False,
        )
        self.assertEqual(value["decision"], p709.PASS)
        broken = self._evaluate(
            "mac-restart",
            runtime_status_after="healthy",
            observer_loaded=True,
            exact_release_consistent=True,
            durable_state_integrity_verified=False,
            historical_effect_replayed=False,
        )
        self.assertEqual(broken["decision"], p709.FAIL_CLOSED)

    def test_unavailable_live_state_uses_isolated_restore_only(self) -> None:
        value = self._evaluate(
            "persistent-state-or-backup-unavailable",
            live_state_available=False,
            live_state_integrity_verified=False,
            verified_backup_available=True,
            isolated_restore_verified=True,
            live_state_overwritten=False,
        )
        self.assertEqual(value["decision"], p709.FORWARD_RECOVERY_REQUIRED)
        self.assertTrue(value["new_effect_authorization_required"])

    def test_live_state_overwrite_is_rejected(self) -> None:
        value = self._evaluate(
            "persistent-state-or-backup-unavailable",
            live_state_available=False,
            live_state_integrity_verified=False,
            verified_backup_available=True,
            isolated_restore_verified=True,
            live_state_overwritten=True,
        )
        self.assertEqual(value["decision"], p709.FAIL_CLOSED)

    def test_network_failure_with_unknown_effect_requires_reconciliation(self) -> None:
        value = self._evaluate(
            "network-proxy-tls-failure",
            connectivity_restored=True,
            tls_trust_verified=True,
            external_effect_state="unknown",
            historical_effect_replayed=False,
        )
        self.assertEqual(value["decision"], p709.RECONCILIATION_REQUIRED)
        self.assertTrue(value["new_effect_authorization_required"])

    def test_network_failure_before_effect_can_recover_technically(self) -> None:
        value = self._evaluate(
            "network-proxy-tls-failure",
            connectivity_restored=True,
            tls_trust_verified=True,
            external_effect_state="none",
            historical_effect_replayed=False,
        )
        self.assertEqual(value["decision"], p709.PASS)
        self.assertFalse(value["consequential_action_authorized_by_drill"])

    def test_product_host_unavailable_never_allows_platform_bypass(self) -> None:
        value = self._evaluate(
            "product-host-unavailable",
            product_host_reachable=True,
            product_contract_boundary_available=True,
            external_effect_state="none",
            platform_bypass_used=True,
        )
        self.assertEqual(value["decision"], p709.FAIL_CLOSED)

    def test_product_host_unknown_external_effect_requires_reconciliation(self) -> None:
        value = self._evaluate(
            "product-host-unavailable",
            product_host_reachable=False,
            product_contract_boundary_available=False,
            external_effect_state="unknown",
            platform_bypass_used=False,
        )
        self.assertEqual(value["decision"], p709.RECONCILIATION_REQUIRED)

    def test_uncertain_external_effect_remains_uncertain_without_verified_evidence(self) -> None:
        value = self._evaluate(
            "uncertain-external-effect",
            external_outcome="unknown",
            reconciliation_evidence_verified=False,
            historical_effect_replayed=False,
            new_effect_authorized=False,
        )
        self.assertEqual(value["decision"], p709.RECONCILIATION_REQUIRED)
        asserted = self._evaluate(
            "uncertain-external-effect",
            external_outcome="confirmed-succeeded",
            reconciliation_evidence_verified=False,
            historical_effect_replayed=False,
            new_effect_authorized=False,
        )
        self.assertEqual(asserted["decision"], p709.RECONCILIATION_REQUIRED)

    def test_confirmed_succeeded_uncertain_effect_is_resolved_without_replay(self) -> None:
        value = self._evaluate(
            "uncertain-external-effect",
            external_outcome="confirmed-succeeded",
            reconciliation_evidence_verified=True,
            historical_effect_replayed=False,
            new_effect_authorized=False,
        )
        self.assertEqual(value["decision"], p709.PASS)
        self.assertFalse(value["historical_external_effect_replay_authorized"])
        self.assertFalse(value["new_effect_authorization_required"])

    def test_confirmed_not_executed_requires_new_effect_authorization(self) -> None:
        value = self._evaluate(
            "uncertain-external-effect",
            external_outcome="confirmed-not-executed",
            reconciliation_evidence_verified=True,
            historical_effect_replayed=False,
            new_effect_authorized=False,
        )
        self.assertEqual(value["decision"], p709.PASS)
        self.assertTrue(value["new_effect_authorization_required"])
        newly_authorized = self._evaluate(
            "uncertain-external-effect",
            external_outcome="confirmed-not-executed",
            reconciliation_evidence_verified=True,
            historical_effect_replayed=False,
            new_effect_authorized=True,
        )
        self.assertEqual(newly_authorized["decision"], p709.PASS)
        self.assertFalse(newly_authorized["new_effect_authorization_required"])
        self.assertIn("new execution", " ".join(newly_authorized["next_actions"]))

    def test_partial_evidence_must_be_complete_integrity_verified_and_attributable(self) -> None:
        value = self._evaluate(
            "partial-evidence-path",
            required_evidence_complete=True,
            integrity_verified=True,
            authoritative_source_known=True,
            fabricated_replacement_evidence=False,
        )
        self.assertEqual(value["decision"], p709.PASS)
        missing = self._evaluate(
            "partial-evidence-path",
            required_evidence_complete=False,
            integrity_verified=False,
            authoritative_source_known=True,
            fabricated_replacement_evidence=False,
        )
        self.assertEqual(missing["decision"], p709.FAIL_CLOSED)

    def test_fabricated_evidence_is_rejected(self) -> None:
        value = self._evaluate(
            "partial-evidence-path",
            required_evidence_complete=True,
            integrity_verified=True,
            authoritative_source_known=True,
            fabricated_replacement_evidence=True,
        )
        self.assertEqual(value["decision"], p709.FAIL_CLOSED)

    def test_credential_rotation_preserves_authority_separation(self) -> None:
        value = self._evaluate(
            "credential-revocation-rotation",
            old_credential_denied=True,
            replacement_credential_verified=True,
            exact_grant_scope_verified=True,
            organizational_authority_inferred_from_access=False,
            reusable_secret_in_evidence=False,
        )
        self.assertEqual(value["decision"], p709.PASS)
        self.assertFalse(value["organizational_authority_satisfied"])
        bad = self._evaluate(
            "credential-revocation-rotation",
            old_credential_denied=True,
            replacement_credential_verified=True,
            exact_grant_scope_verified=True,
            organizational_authority_inferred_from_access=True,
            reusable_secret_in_evidence=False,
        )
        self.assertEqual(bad["decision"], p709.FAIL_CLOSED)

    def test_failed_update_rollback_passes_only_after_exact_healthy_recovery(self) -> None:
        value = self._evaluate(
            "failed-update-rollback",
            active_release_known=True,
            latest_transaction_known=True,
            state_schema_changed=False,
            rollback_safe=True,
            rollback_completed=True,
            runtime_healthy_after=True,
            observer_release_consistent=True,
            historical_effect_replayed=False,
        )
        self.assertEqual(value["decision"], p709.PASS)
        incomplete = self._evaluate(
            "failed-update-rollback",
            active_release_known=True,
            latest_transaction_known=True,
            state_schema_changed=False,
            rollback_safe=True,
            rollback_completed=False,
            runtime_healthy_after=False,
            observer_release_consistent=False,
            historical_effect_replayed=False,
        )
        self.assertEqual(incomplete["decision"], p709.FAIL_CLOSED)

    def test_schema_changed_update_requires_forward_recovery(self) -> None:
        value = self._evaluate(
            "failed-update-rollback",
            active_release_known=True,
            latest_transaction_known=True,
            state_schema_changed=True,
            rollback_safe=False,
            rollback_completed=False,
            runtime_healthy_after=False,
            observer_release_consistent=False,
            historical_effect_replayed=False,
        )
        self.assertEqual(value["decision"], p709.FORWARD_RECOVERY_REQUIRED)

    def test_common_guards_reject_secret_authority_scope_and_effect_leakage(self) -> None:
        base = {
            **self._common(),
            "runtime_status_after": "healthy",
            "exact_release_verified": True,
            "supervised_generation_advanced": True,
            "historical_effect_replayed": False,
        }
        for key, value in (
            ("operator_attributable", False),
            ("organization_scope_verified", False),
            ("reusable_secret_exposed", True),
            ("canonical_mutation_by_drill", True),
            ("external_effect_invoked_by_drill", True),
        ):
            bad = dict(base)
            bad[key] = value
            with self.subTest(key=key), self.assertRaises(p709.BoundaryError):
                p709.evaluate("runtime-crash", bad)

    def test_unknown_and_missing_evidence_fields_fail_closed_at_boundary(self) -> None:
        evidence = {
            **self._common(),
            "runtime_status_after": "healthy",
            "exact_release_verified": True,
            "supervised_generation_advanced": True,
            "historical_effect_replayed": False,
        }
        with self.assertRaises(p709.BoundaryError):
            p709.evaluate("runtime-crash", {**evidence, "surprise": True})
        del evidence["exact_release_verified"]
        with self.assertRaises(p709.BoundaryError):
            p709.evaluate("runtime-crash", evidence)

    def test_record_and_verify_drill_receipt(self) -> None:
        evidence = {
            **self._common(),
            "external_outcome": "unknown",
            "reconciliation_evidence_verified": False,
            "historical_effect_replayed": False,
            "new_effect_authorized": False,
        }
        result = p709.record_drill(
            "uncertain-external-effect",
            evidence,
            repository_sha=self.release_sha,
            output_dir=self.root,
            expected_decision=p709.RECONCILIATION_REQUIRED,
        )
        self.assertEqual(result["status"], "PASS")
        receipt = Path(result["receipt"])
        digest = Path(result["digest_file"])
        self.assertEqual(hashlib.sha256(receipt.read_bytes()).hexdigest(), result["receipt_sha256"])
        verified = p709.verify_receipt(receipt, digest)
        self.assertEqual(verified["status"], "PASS")
        self.assertEqual(verified["drill_status"], "PASS")

    def test_record_mismatched_expectation_is_failed_drill_evidence_not_rewritten(self) -> None:
        evidence = {
            **self._common(),
            "runtime_status_after": "healthy",
            "exact_release_verified": True,
            "supervised_generation_advanced": True,
            "historical_effect_replayed": False,
        }
        result = p709.record_drill(
            "runtime-crash",
            evidence,
            repository_sha=self.release_sha,
            output_dir=self.root,
            expected_decision=p709.FAIL_CLOSED,
        )
        self.assertEqual(result["status"], "FAIL")
        verified = p709.verify_receipt(Path(result["receipt"]), Path(result["digest_file"]))
        self.assertEqual(verified["drill_status"], "FAIL")

    def test_receipt_tamper_is_detected(self) -> None:
        evidence = {
            **self._common(),
            "runtime_status_after": "healthy",
            "exact_release_verified": True,
            "supervised_generation_advanced": True,
            "historical_effect_replayed": False,
        }
        result = p709.record_drill(
            "runtime-crash",
            evidence,
            repository_sha=self.release_sha,
            output_dir=self.root,
            expected_decision=p709.PASS,
        )
        receipt = Path(result["receipt"])
        receipt.write_text(receipt.read_text(encoding="utf-8") + " ", encoding="utf-8")
        with self.assertRaises(p709.BoundaryError):
            p709.verify_receipt(receipt, Path(result["digest_file"]))


if __name__ == "__main__":
    unittest.main()
