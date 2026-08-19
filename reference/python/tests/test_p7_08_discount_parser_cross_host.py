from __future__ import annotations

import hashlib
import inspect
import json
import tempfile
import unittest
from pathlib import Path

from arvectum_os_ref.product_capability_consumption import CAP_004_AUDIT_RECONSTRUCTION
from p6_07_discount_parser_ref.contract import (
    P6_06_CANONICAL_BLOB_SHA,
    PRODUCT_CONTRACT_VERSION,
)
import p7_08_discount_parser_cross_host as p708


class P708DiscountParserCrossHostContourTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        self.runtime_root = self.root / "mac-runtime"
        self.windows_root = self.root / "windows"
        self.windows_root.mkdir()
        self.execution_id = "p7-08-test-execution-001"
        self.release_sha = "a" * 40
        self.product_sha = "b" * 40

    def _write_evidence(self, name: str, payload: bytes) -> tuple[Path, Path]:
        path = self.windows_root / name
        digest_path = self.windows_root / f"{name}.sha256"
        path.write_bytes(payload)
        digest = hashlib.sha256(payload).hexdigest()
        digest_path.write_text(f"{digest}  {name}\n", encoding="utf-8")
        return path, digest_path

    def _descriptor(self) -> dict:
        return {
            "schema": p708.DESCRIPTOR_SCHEMA,
            "schema_version": p708.DESCRIPTOR_SCHEMA_VERSION,
            "product": {
                "repository": p708.PRODUCT_REPOSITORY,
                "repository_sha": self.product_sha,
            },
            "candidate": {
                "offer_id": "offer-901",
                "status_before": "ready",
                "text_only": True,
            },
            "target_ref": "@arvectumtest",
            "template_version": "v2-configurable",
            "authorization": {
                "type": "explicit-human-one-time",
                "received": True,
                "authorized_at": "2026-08-19T09:00:00Z",
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
                "publication_id": "publication-77",
                "reservation_status": "pending",
            },
            "outcome": {
                "publish_result_status": "published",
                "publication_status": "published",
                "offer_status": "published",
                "telegram_message_id": "message-501",
                "external_confirmation": "PASS",
                "reconciliation_required": False,
            },
            "material_refs": [
                {"role": "parse-run", "reference": "parse-run-2026-08-19-001"},
                {"role": "source-observation", "reference": "source-observation-901"},
                {"role": "offer", "reference": "offer-901"},
                {"role": "publication-candidate", "reference": "candidate-offer-901"},
                {"role": "filter-config", "reference": "telegram-default-filter-v4"},
                {"role": "template-version", "reference": "v2-configurable"},
                {"role": "publication-reservation", "reference": "publication-77-pending"},
                {"role": "publication-attempt", "reference": "publication-77-attempt-1"},
                {"role": "telegram-target", "reference": "@arvectumtest"},
                {
                    "role": "authorization-evidence",
                    "reference": "explicit-human-one-time/2026-08-19T09:00:00Z/offer-901/@arvectumtest",
                },
            ],
        }

    def _issue(self) -> dict:
        return p708.issue_dispatch(
            runtime_root=self.runtime_root,
            organization_id="p708-test-org",
            actor_id="p708-human",
            canonical_repo_sha=self.release_sha,
            execution_id=self.execution_id,
        )

    def _handoff(self, descriptor: dict | None = None, *, suffix: str = "one") -> dict:
        issued = self._issue() if not (self.runtime_root / "product-contours").exists() else None
        if issued is None:
            run_root = (
                self.runtime_root
                / "product-contours"
                / "discount-parser"
                / "runs"
                / self.execution_id
                / "outbound"
            )
            dispatch_path = run_root / p708.DISPATCH_FILENAME
            dispatch_digest_path = run_root / p708.DISPATCH_DIGEST_FILENAME
        else:
            dispatch_path = issued["dispatch_path"]
            dispatch_digest_path = issued["dispatch_digest_path"]

        descriptor_path = self.windows_root / f"descriptor-{suffix}.json"
        descriptor_path.write_text(
            json.dumps(descriptor or self._descriptor(), ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        pre, pre_digest = self._write_evidence(f"pre-{suffix}.json", f"pre-effect-{suffix}".encode())
        outcome, outcome_digest = self._write_evidence(f"outcome-{suffix}.json", f"outcome-{suffix}".encode())
        return p708.prepare_windows_handoff(
            dispatch_path=dispatch_path,
            dispatch_digest_path=dispatch_digest_path,
            descriptor_path=descriptor_path,
            pre_effect_path=pre,
            pre_effect_digest_path=pre_digest,
            outcome_path=outcome,
            outcome_digest_path=outcome_digest,
            output_dir=self.windows_root / f"handoff-{suffix}",
        )

    def test_issue_keeps_identity_mac_private_and_dispatch_is_minimized(self) -> None:
        result = self._issue()
        dispatch = json.loads(Path(result["dispatch_path"]).read_text(encoding="utf-8"))
        serialized = json.dumps(dispatch, ensure_ascii=False)
        self.assertNotIn("p708-test-org", serialized)
        self.assertNotIn("p708-human", serialized)
        self.assertEqual(dispatch["product_contract"]["version"], PRODUCT_CONTRACT_VERSION)
        self.assertEqual(dispatch["product_contract"]["blob_sha"], P6_06_CANONICAL_BLOB_SHA)
        self.assertEqual(dispatch["product_contract"]["shared_dependencies"], ["CAP-004"])
        self.assertFalse(dispatch["cross_host_boundary"]["mutable_shared_state_required"])
        ticket_text = Path(result["ticket_path"]).read_text(encoding="utf-8")
        self.assertIn("p708-test-org", ticket_text)
        self.assertIn("p708-human", ticket_text)

    def test_windows_handoff_binds_raw_evidence_without_transferring_it(self) -> None:
        result = self._handoff()
        payload = json.loads(Path(result["handoff_path"]).read_text(encoding="utf-8"))
        serialized = json.dumps(payload, ensure_ascii=False)
        self.assertNotIn("pre-effect-one", serialized)
        self.assertNotIn("outcome-one", serialized)
        self.assertNotIn("p708-test-org", serialized)
        self.assertNotIn("p708-human", serialized)
        self.assertEqual(payload["product_contract"]["shared_dependencies"], ["CAP-004"])
        self.assertFalse(payload["replay_safety"]["external_effect_replay_permitted"])
        self.assertEqual(payload["replay_safety"]["reconstruction_side_effect_class"], "ReadOnly")

    def test_secret_or_identity_over_transfer_fails_closed(self) -> None:
        self._issue()
        descriptor = self._descriptor()
        descriptor["target_ref"] = "@arvectumtest?token=do-not-transfer"
        descriptor_path = self.windows_root / "descriptor-secret.json"
        descriptor_path.write_text(json.dumps(descriptor), encoding="utf-8")
        pre, pre_digest = self._write_evidence("pre-secret.json", b"pre-secret")
        out, out_digest = self._write_evidence("out-secret.json", b"out-secret")
        dispatch_root = (
            self.runtime_root / "product-contours" / "discount-parser" / "runs" / self.execution_id / "outbound"
        )
        with self.assertRaises(p708.P708ContourError):
            p708.prepare_windows_handoff(
                dispatch_path=dispatch_root / p708.DISPATCH_FILENAME,
                dispatch_digest_path=dispatch_root / p708.DISPATCH_DIGEST_FILENAME,
                descriptor_path=descriptor_path,
                pre_effect_path=pre,
                pre_effect_digest_path=pre_digest,
                outcome_path=out,
                outcome_digest_path=out_digest,
                output_dir=self.windows_root / "bad-secret-handoff",
            )

    def test_uncertain_external_outcome_fails_closed(self) -> None:
        self._issue()
        descriptor = self._descriptor()
        descriptor["outcome"]["external_confirmation"] = "UNCERTAIN"
        descriptor["outcome"]["reconciliation_required"] = True
        descriptor_path = self.windows_root / "descriptor-uncertain.json"
        descriptor_path.write_text(json.dumps(descriptor), encoding="utf-8")
        pre, pre_digest = self._write_evidence("pre-uncertain.json", b"pre-uncertain")
        out, out_digest = self._write_evidence("out-uncertain.json", b"out-uncertain")
        dispatch_root = (
            self.runtime_root / "product-contours" / "discount-parser" / "runs" / self.execution_id / "outbound"
        )
        with self.assertRaises(p708.P708ContourError):
            p708.prepare_windows_handoff(
                dispatch_path=dispatch_root / p708.DISPATCH_FILENAME,
                dispatch_digest_path=dispatch_root / p708.DISPATCH_DIGEST_FILENAME,
                descriptor_path=descriptor_path,
                pre_effect_path=pre,
                pre_effect_digest_path=pre_digest,
                outcome_path=out,
                outcome_digest_path=out_digest,
                output_dir=self.windows_root / "bad-uncertain-handoff",
            )

    def test_tampered_dispatch_fails_closed(self) -> None:
        issued = self._issue()
        dispatch_path = Path(issued["dispatch_path"])
        payload = json.loads(dispatch_path.read_text(encoding="utf-8"))
        payload["execution_id"] = "tampered"
        dispatch_path.write_text(json.dumps(payload), encoding="utf-8")
        descriptor_path = self.windows_root / "descriptor-tampered.json"
        descriptor_path.write_text(json.dumps(self._descriptor()), encoding="utf-8")
        pre, pre_digest = self._write_evidence("pre-tampered.json", b"pre")
        out, out_digest = self._write_evidence("out-tampered.json", b"out")
        with self.assertRaises(p708.P708ContourError):
            p708.prepare_windows_handoff(
                dispatch_path=dispatch_path,
                dispatch_digest_path=issued["dispatch_digest_path"],
                descriptor_path=descriptor_path,
                pre_effect_path=pre,
                pre_effect_digest_path=pre_digest,
                outcome_path=out,
                outcome_digest_path=out_digest,
                output_dir=self.windows_root / "bad-tampered-handoff",
            )

    def test_end_to_end_reconstruction_is_cap004_only_read_only_and_identity_minimized(self) -> None:
        handoff = self._handoff()
        result = p708.reconstruct_on_mac(
            runtime_root=self.runtime_root,
            handoff_path=handoff["handoff_path"],
            handoff_digest_path=handoff["handoff_digest_path"],
            canonical_repo_sha=self.release_sha,
        )
        self.assertEqual(result["status"], "PASS")
        report = json.loads(Path(result["report_path"]).read_text(encoding="utf-8"))
        serialized = json.dumps(report, ensure_ascii=False)
        self.assertNotIn("p708-test-org", serialized)
        self.assertNotIn("p708-human", serialized)
        self.assertEqual(report["continuity"]["shared_dependencies"], ["CAP-004"])
        self.assertTrue(report["cap004"]["read_only"])
        self.assertTrue(report["cap004"]["reconstruction_complete"])
        self.assertEqual(report["containment"]["external_mutations"], 0)
        self.assertFalse(report["containment"]["telegram_effect_replayed"])
        self.assertFalse(report["cap004"]["derived_observation_is_canonical_event"])

        second = p708.reconstruct_on_mac(
            runtime_root=self.runtime_root,
            handoff_path=handoff["handoff_path"],
            handoff_digest_path=handoff["handoff_digest_path"],
            canonical_repo_sha=self.release_sha,
        )
        self.assertEqual(second["status"], "ALREADY_RECONSTRUCTED")

    def test_different_handoff_for_completed_execution_is_rejected(self) -> None:
        first = self._handoff(suffix="one")
        p708.reconstruct_on_mac(
            runtime_root=self.runtime_root,
            handoff_path=first["handoff_path"],
            handoff_digest_path=first["handoff_digest_path"],
            canonical_repo_sha=self.release_sha,
        )
        descriptor = self._descriptor()
        descriptor["candidate"]["offer_id"] = "offer-902"
        descriptor["material_refs"] = [
            {**row, "reference": row["reference"].replace("901", "902")}
            for row in descriptor["material_refs"]
        ]
        second = self._handoff(descriptor, suffix="two")
        with self.assertRaises(p708.P708ContourError):
            p708.reconstruct_on_mac(
                runtime_root=self.runtime_root,
                handoff_path=second["handoff_path"],
                handoff_digest_path=second["handoff_digest_path"],
                canonical_repo_sha=self.release_sha,
            )

    def test_source_has_no_live_network_or_external_effect_path(self) -> None:
        source = inspect.getsource(p708).lower()
        for forbidden in (
            "import requests",
            "import httpx",
            "from aiogram",
            "publish_offer(",
            "send_message(",
            "send_photo(",
            "api.telegram.org",
            "telegram_bot_token",
        ):
            self.assertNotIn(forbidden, source)

    def test_product_contract_projection_remains_cap004_only(self) -> None:
        issued = self._issue()
        ticket = json.loads(Path(issued["ticket_path"]).read_text(encoding="utf-8"))
        self.assertEqual(ticket["product_contract"]["shared_dependencies"], ["CAP-004"])
        self.assertEqual(ticket["product_contract"]["version"], PRODUCT_CONTRACT_VERSION)
        self.assertEqual(ticket["product_contract"]["blob_sha"], P6_06_CANONICAL_BLOB_SHA)
        self.assertEqual(CAP_004_AUDIT_RECONSTRUCTION.value, "CAP-004")


if __name__ == "__main__":
    unittest.main()
