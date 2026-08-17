from __future__ import annotations

import hashlib
import inspect
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from arvectum_os_ref.identity import Identity
from arvectum_os_ref.product_capability_consumption import CAP_004_AUDIT_RECONSTRUCTION
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import OperationSideEffectClass
from p6_07_discount_parser_ref.contract import P6_06_CANONICAL_BLOB_SHA, PRODUCT_CONTRACT_VERSION
import p6_07_discount_parser_ref.stage2c as stage2c


class P607Stage2CCap004ReconstructionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        self.organization = OrganizationScope(Identity("organization", "stage2c-org", "platform"))
        self.actor = ActorContext(
            Principal(Identity("principal", "stage2c-human", "stage2c-org")),
            self.organization,
        )
        self.ticket = {"created_at": "2026-08-17T08:51:09Z"}

    def _material_rows(self) -> list[dict[str, str]]:
        return [
            {"role": "parse-run", "reference": "parse-run-stage2b-source"},
            {"role": "source-observation", "reference": "offer-148-source-observation"},
            {"role": "offer", "reference": "offer-148"},
            {"role": "publication-candidate", "reference": "candidate-offer-148"},
            {"role": "filter-config", "reference": "telegram-default-stage2b-snapshot"},
            {"role": "template-version", "reference": "v2-configurable"},
            {"role": "publication-reservation", "reference": "publication-14-pending"},
            {"role": "publication-attempt", "reference": "publication-14-attempt-1"},
            {"role": "telegram-target", "reference": "@arvectumtest"},
            {
                "role": "authorization-evidence",
                "reference": "explicit-human-one-time/2026-08-17T11:07:09Z/offer-148/@arvectumtest",
            },
        ]

    def _handoff(self) -> dict:
        return {
            "schema": stage2c.STAGE2B_HANDOFF_SCHEMA,
            "schema_version": stage2c.STAGE2B_HANDOFF_SCHEMA_VERSION,
            "execution_id": stage2c.EXPECTED_EXECUTION_ID,
            "stage2a_ticket_sha256": stage2c.EXPECTED_STAGE2A_TICKET_SHA256,
            "product_contract": {
                "version": PRODUCT_CONTRACT_VERSION,
                "blob_sha": P6_06_CANONICAL_BLOB_SHA,
            },
            "canonical_stage2b_review": {
                "path": stage2c.STAGE2B_REVIEW_PATH,
                "blob_sha": stage2c.STAGE2B_REVIEW_BLOB_SHA,
                "closure_commit": stage2c.STAGE2B_CLOSURE_COMMIT,
            },
            "product": {
                "repository": stage2c.STAGE2B_PRODUCT_REPOSITORY,
                "repository_sha": stage2c.STAGE2B_PRODUCT_SHA,
            },
            "candidate": {"offer_id": "148", "status_before": "ready", "text_only": True},
            "target_ref": "@arvectumtest",
            "template_version": "v2-configurable",
            "authorization": {
                "type": "explicit-human-one-time",
                "received": True,
                "authorized_at": "2026-08-17T11:07:09Z",
                "scope_matches_candidate_target": True,
                "max_external_sends": 1,
            },
            "containment": {
                "scheduler_disabled": True,
                "autopost_disabled": True,
                "other_publishers_running": False,
                "publish_offer_invocations": 1,
                "telegram_send_delegations": 1,
                "telegram_send_message_calls": 1,
                "telegram_send_photo_calls": 0,
            },
            "pre_effect": {
                "sha256": stage2c.STAGE2B_PRE_EFFECT_SHA256,
                "publication_id": "14",
                "reservation_status": "pending",
            },
            "outcome": {
                "sha256": stage2c.STAGE2B_OUTCOME_SHA256,
                "publish_result_status": "published",
                "publication_status": "published",
                "offer_status": "published",
                "telegram_message_id": "27",
                "external_confirmation": "PASS",
                "reconciliation_required": False,
            },
            "material_refs": self._material_rows(),
            "data_minimization": {
                "raw_pre_effect_embedded": False,
                "raw_outcome_embedded": False,
                "reusable_secrets_embedded": False,
                "raw_opaque_organization_identity_embedded": False,
                "raw_opaque_actor_identity_embedded": False,
            },
        }

    def _write_handoff(self, payload: dict | None = None) -> tuple[Path, Path]:
        payload = payload or self._handoff()
        raw = (json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        json_path = self.root / stage2c.STAGE2B_HANDOFF_FILENAME
        digest_path = self.root / stage2c.STAGE2B_HANDOFF_DIGEST_FILENAME
        json_path.write_bytes(raw)
        digest_path.write_text(f"{digest}  {stage2c.STAGE2B_HANDOFF_FILENAME}\n", encoding="utf-8")
        return json_path, digest_path

    def _reconstruct(self, payload: dict | None = None):
        handoff, digest = self._write_handoff(payload)
        with patch.object(
            stage2c,
            "_load_stage2a_context",
            return_value=(self.ticket, self.organization, self.actor),
        ):
            return stage2c.reconstruct_stage2b_through_cap004(
                stage2a_ticket_path=self.root / stage2c.STAGE2A_TICKET_FILENAME,
                stage2a_digest_path=self.root / stage2c.STAGE2A_DIGEST_FILENAME,
                stage2b_handoff_path=handoff,
                stage2b_handoff_digest_path=digest,
                canonical_repo_sha="a" * 40,
            )

    def test_real_minimized_stage2b_handoff_reconstructs_through_cap004(self) -> None:
        result = self._reconstruct()
        self.assertTrue(result.reconstruction.complete)
        self.assertEqual(result.reconstruction.organization, self.organization)
        self.assertEqual(result.reconstruction.initiating_actor_id, self.actor.actual_principal.principal_id)
        self.assertEqual(result.manifest.execution_subject_id.value, stage2c.EXPECTED_EXECUTION_ID)
        self.assertEqual(result.manifest.product_contract, result.adapters.facade.context.product_contract)
        self.assertEqual(result.manifest.gate_decisions, ())
        self.assertEqual(result.report["stage2b"]["telegram_message_id"], "27")
        self.assertEqual(result.report["stage2b"]["external_confirmation"], "PASS")
        self.assertTrue(result.report["cap004"]["read_only"])
        self.assertTrue(result.report["cap004"]["reconstruction_complete"])
        self.assertEqual(result.report["containment"]["telegram_calls"], 0)
        self.assertFalse(result.report["containment"]["telegram_effect_replayed"])

    def test_projection_remains_cap004_only_and_read_only(self) -> None:
        result = self._reconstruct()
        contract = result.adapters.facade.context.contract
        self.assertEqual({item.dependency_id for item in contract.dependencies}, {CAP_004_AUDIT_RECONSTRUCTION})
        self.assertTrue(all(item.provisional for item in contract.dependencies))
        self.assertTrue(
            all(
                item.side_effect_classes == (OperationSideEffectClass.READ_ONLY,)
                and not item.canonical_accesses
                for item in contract.operations
            )
        )

    def test_handoff_builder_binds_opaque_raw_evidence_without_embedding_it(self) -> None:
        pre = self.root / "pre-effect.json"
        outcome = self.root / "outcome.json"
        pre.write_bytes(b"opaque-pre-effect-evidence")
        outcome.write_bytes(b"opaque-outcome-evidence")
        pre_sha = hashlib.sha256(pre.read_bytes()).hexdigest()
        out_sha = hashlib.sha256(outcome.read_bytes()).hexdigest()
        rows = tuple(f"{row['role']}={row['reference']}" for row in self._material_rows())
        handoff = stage2c.build_stage2b_minimized_handoff(
            pre_effect_path=pre,
            outcome_path=outcome,
            material_refs=rows,
            expected_pre_effect_sha256=pre_sha,
            expected_outcome_sha256=out_sha,
        )
        self.assertEqual(handoff["pre_effect"]["sha256"], pre_sha)
        self.assertEqual(handoff["outcome"]["sha256"], out_sha)
        serialized = json.dumps(handoff)
        self.assertNotIn("opaque-pre-effect-evidence", serialized)
        self.assertNotIn("opaque-outcome-evidence", serialized)
        self.assertFalse(handoff["data_minimization"]["raw_pre_effect_embedded"])
        self.assertFalse(handoff["data_minimization"]["raw_outcome_embedded"])

    def test_wrong_stage2b_pre_effect_digest_fails_closed(self) -> None:
        payload = self._handoff()
        payload["pre_effect"]["sha256"] = "0" * 64
        with self.assertRaises(stage2c.Stage2CError):
            self._reconstruct(payload)

    def test_wrong_execution_or_contract_continuity_fails_closed(self) -> None:
        wrong_execution = self._handoff()
        wrong_execution["execution_id"] = "different-execution"
        with self.assertRaises(stage2c.Stage2CError):
            self._reconstruct(wrong_execution)

        wrong_contract = self._handoff()
        wrong_contract["product_contract"]["blob_sha"] = "0" * 40
        with self.assertRaises(stage2c.Stage2CError):
            self._reconstruct(wrong_contract)

    def test_unconfirmed_or_uncertain_external_outcome_fails_closed(self) -> None:
        unconfirmed = self._handoff()
        unconfirmed["outcome"]["external_confirmation"] = "UNCERTAIN"
        with self.assertRaises(stage2c.Stage2CError):
            self._reconstruct(unconfirmed)

        uncertain = self._handoff()
        uncertain["outcome"]["reconciliation_required"] = True
        with self.assertRaises(stage2c.Stage2CError):
            self._reconstruct(uncertain)

    def test_missing_material_source_or_rule_reference_fails_closed(self) -> None:
        missing_source = self._handoff()
        missing_source["material_refs"] = [
            row for row in missing_source["material_refs"] if row["role"] != "source-observation"
        ]
        with self.assertRaises(stage2c.Stage2CError):
            self._reconstruct(missing_source)

        missing_rule = self._handoff()
        missing_rule["material_refs"] = [
            row for row in missing_rule["material_refs"] if row["role"] not in {"rule-config", "filter-config"}
        ]
        with self.assertRaises(stage2c.Stage2CError):
            self._reconstruct(missing_rule)

    def test_stage2c_source_has_no_external_effect_or_live_network_path(self) -> None:
        source = inspect.getsource(stage2c).lower()
        for forbidden in (
            "import requests",
            "import httpx",
            "from aiogram",
            "publish_offer(",
            "send_message(",
            "send_photo(",
            "faketelegramadapter",
            "telegram_bot_token",
            "api.telegram.org",
        ):
            self.assertNotIn(forbidden, source)
        self.assertIn('"telegram_calls": 0', source)
        self.assertIn('"external_mutations": 0', source)

    def test_stage2c_report_excludes_raw_stage2a_identity_values(self) -> None:
        result = self._reconstruct()
        serialized = json.dumps(result.report, ensure_ascii=False)
        self.assertNotIn("stage2c-org", serialized)
        self.assertNotIn("stage2c-human", serialized)
        self.assertEqual(result.report["continuity"]["organization_continuity"], "PASS")
        self.assertEqual(result.report["continuity"]["actor_continuity"], "PASS")


if __name__ == "__main__":
    unittest.main()
