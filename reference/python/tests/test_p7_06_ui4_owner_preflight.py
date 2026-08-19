from __future__ import annotations

import io
import json
import os
import pathlib
import stat
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from arvectum_os_ref.identity import Identity

import p7_03_durable_state as p703
import p7_06_ui1_live_workspace as ui1
import p7_06_ui2_governed_interaction as ui2
import p7_06_ui4_owner_preflight as ui4


RELEASE = "d" * 40


class UI4OwnerPreflightTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name) / "runtime"
        self.org = Identity("organization", "arvectum-test", "platform")
        self.human = Identity("principal", "owner-human", self.org.value)
        self.subject = "document-subject/eis-0344100006426000005-exact-attachment-evidence@arvectum-test"
        self.version = "document-version/eis-0344100006426000005-74e943d855406b04@arvectum-test"
        self.execution_subject = "execution-subject/p7-06-ui1-real-state-74e943d855406b04@arvectum-test"
        self.execution_version = "execution-version/p7-06-ui1-real-state-74e943d855406b04-v5@arvectum-test"
        self.event_version = "event-version/p7-06-ui1-document-admitted-74e943d855406b04-v1@arvectum-test"
        self.event_subject = "event-subject/p7-06-ui1-document-admitted-74e943d855406b04@arvectum-test"
        self.metadata = {
            "state_class": "canonical-governed-state",
            "organization_scope": p703.ORGANIZATION_SCOPE,
            "semantic_type": "platform.document",
            "schema_version": "p7.06-ui1-real-eis-evidence-1",
            "classification": "restricted-pilot",
            "retention_policy_ref": "P6.02 restricted-paid-pilot / inherit-product-source-retention",
            "source_release_sha": RELEASE,
            "subject_identity": self.subject,
            "version_identity": self.version,
            "authority_mode": "External Reference",
            "authority_scope": "product.document/external-authority",
            "authoritative_source": "ЕИС / zakupki.gov.ru",
            "validation_status": "CAP-001 admitted; RFC-0006 provenance admitted; CAP-004 reconstruction complete",
            "governed_admission_ref": self.event_version,
            "provenance_refs": [
                "principal/owner-human@arvectum-test",
                self.execution_subject,
                self.execution_version,
                self.event_subject,
                self.event_version,
                "sha256:" + "7" * 64,
            ],
            "source_manifest_sha256": "7" * 64,
            "product_contract_version": "0.1.0",
            "canonical_authority": True,
            "contains_reusable_secret": False,
            "raw_document_bytes_included": False,
            "external_actions": False,
        }
        self.payload = {
            "schema": ui4.TARGET_PAYLOAD_SCHEMA,
            "subject_identity": self.subject,
            "version_identity": self.version,
            "semantic_type": "platform.document",
            "schema_version": "p7.06-ui1-real-eis-evidence-1",
            "authority_mode": "External Reference",
            "authority_scope": "product.document/external-authority",
            "authoritative_system": "ЕИС / zakupki.gov.ru",
            "external_object_ref": "44fz-notice:0344100006426000005",
            "manifest_sha256": "7" * 64,
            "member_count": 7,
            "product_contract_subject": "product-contract/tender@arvectum-test",
            "product_contract_version": "product-contract-version/tender-v0.1.0@arvectum-test",
            "execution_subject": self.execution_subject,
            "execution_version": self.execution_version,
            "event_subject": self.event_subject,
            "event_version": self.event_version,
            "provenance_refs": ["principal/owner-human@arvectum-test"],
            "artifact_integrity_refs": ["sha256:" + "7" * 64],
            "raw_document_bytes_included": False,
            "reusable_secret_included": False,
            "external_actions": False,
        }
        item_id = p703.persist_governed_item(
            self.root,
            RELEASE,
            json.dumps(self.payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"),
            self.metadata,
        )
        self.item_id = item_id
        self.checkpoint_id = "checkpoint-ui4"
        workspace = SimpleNamespace(
            organization=SimpleNamespace(organization_id=SimpleNamespace(value=self.org.value)),
            actor=SimpleNamespace(actual_principal=SimpleNamespace(principal_id=SimpleNamespace(value=self.human.value))),
        )
        self.snapshot = ui1.LiveWorkspaceSnapshot(
            workspace=workspace,
            runtime_root=self.root,
            release_sha=RELEASE,
            health_state="healthy",
            health_code="P7_05_HEALTHY",
            health_detail="healthy",
            heartbeat_age_seconds=0.1,
            items=(
                ui1.LiveGovernedItem(
                    storage_item_id=item_id,
                    semantic_type=self.metadata["semantic_type"],
                    schema_version=self.metadata["schema_version"],
                    subject_identity=self.subject,
                    version_identity=self.version,
                    authority_mode=self.metadata["authority_mode"],
                    authority_scope=self.metadata["authority_scope"],
                    authoritative_source=self.metadata["authoritative_source"],
                    classification=self.metadata["classification"],
                    lifecycle_status=None,
                    validation_status=self.metadata["validation_status"],
                    governed_admission_ref=self.event_version,
                    provenance_refs=tuple(self.metadata["provenance_refs"]),
                    source_release_sha=RELEASE,
                ),
            ),
            checkpoints=(
                ui1.LiveCheckpoint(
                    checkpoint_id=self.checkpoint_id,
                    execution_subject_identity=self.execution_subject,
                    execution_version_identity=self.execution_version,
                    classification="restricted-pilot",
                    reason="P7.06-UI1 first real retained governed item admission",
                    governed_storage_item_ids=(item_id,),
                ),
            ),
            access_grant_id="inspect-grant",
        )
        self.credential_file = self.root / "credential.secret"
        self.credential_file.write_text("not-read-by-patched-test", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def _technical_access(self):
        return SimpleNamespace(
            allowed=True,
            principal_kind="human",
            organizational_authority_satisfied=False,
            consequential_approval_satisfied=False,
            grant_id="interaction-grant",
        )

    def _build(self):
        with patch.object(ui1, "build_live_snapshot", return_value=self.snapshot), patch.object(
            ui2, "_authorize_interaction", return_value=self._technical_access()
        ):
            return ui4.build_owner_preflight(
                self.root,
                organization=self.org,
                principal=self.human,
                credential_id="credential-1",
                credential_file=self.credential_file,
            )

    def test_real_retained_preflight_is_waiting_and_keeps_technical_access_separate(self):
        result = self._build()
        self.assertEqual(result.outcome, "Waiting")
        self.assertEqual(result.technical_interaction_access, "PASS")
        self.assertEqual(result.subject_identity, self.subject)
        self.assertEqual(result.version_identity, self.version)
        self.assertEqual(result.execution_version, self.execution_version)
        self.assertEqual(result.event_version, self.event_version)
        self.assertEqual(result.checkpoint_id, self.checkpoint_id)
        self.assertEqual([row.name for row in result.gates], [
            "Authorization", "Organizational Authority", "Data Governance", "Consequential Approval"
        ])
        self.assertTrue(all(row.state == "Waiting" for row in result.gates))
        self.assertFalse(result.canonical_mutation_requested)
        self.assertFalse(result.external_effect_requested)

    def test_payload_claiming_external_action_fails_closed(self):
        item_dir = self.root / "state" / "governed" / "items" / self.item_id
        payload = dict(self.payload)
        payload["external_actions"] = True
        bad_id = p703.persist_governed_item(
            self.root,
            RELEASE,
            json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"),
            self.metadata,
        )
        bad_item = self.snapshot.items[0]
        bad_item = ui1.LiveGovernedItem(
            storage_item_id=bad_id,
            semantic_type=bad_item.semantic_type,
            schema_version=bad_item.schema_version,
            subject_identity=bad_item.subject_identity,
            version_identity=bad_item.version_identity,
            authority_mode=bad_item.authority_mode,
            authority_scope=bad_item.authority_scope,
            authoritative_source=bad_item.authoritative_source,
            classification=bad_item.classification,
            lifecycle_status=bad_item.lifecycle_status,
            validation_status=bad_item.validation_status,
            governed_admission_ref=bad_item.governed_admission_ref,
            provenance_refs=bad_item.provenance_refs,
            source_release_sha=bad_item.source_release_sha,
        )
        bad_snapshot = ui1.LiveWorkspaceSnapshot(
            workspace=self.snapshot.workspace,
            runtime_root=self.root,
            release_sha=RELEASE,
            health_state="healthy",
            health_code="P7_05_HEALTHY",
            health_detail="healthy",
            heartbeat_age_seconds=0.1,
            items=(bad_item,),
            checkpoints=(ui1.LiveCheckpoint(
                checkpoint_id=self.checkpoint_id,
                execution_subject_identity=self.execution_subject,
                execution_version_identity=self.execution_version,
                classification="restricted-pilot",
                reason="proof",
                governed_storage_item_ids=(bad_id,),
            ),),
            access_grant_id="inspect-grant",
        )
        with patch.object(ui1, "build_live_snapshot", return_value=bad_snapshot), patch.object(
            ui2, "_authorize_interaction", return_value=self._technical_access()
        ):
            with self.assertRaises(ui4.UI4IntegrityError):
                ui4.build_owner_preflight(
                    self.root,
                    organization=self.org,
                    principal=self.human,
                    credential_id="credential-1",
                    credential_file=self.credential_file,
                )
        self.assertTrue(item_dir.is_dir())

    def test_render_exposes_real_chain_but_no_action_authority(self):
        result = self._build()
        html = ui4.render_owner_preflight_html(result, csrf_token="csrf-test")
        self.assertIn(self.subject, html)
        self.assertIn(self.version, html)
        self.assertIn(self.execution_version, html)
        self.assertIn(self.event_version, html)
        self.assertIn("Run governed preflight", html)
        self.assertIn("Outcome: Waiting", html)
        self.assertIn("workspace.interact is technical access only", html)
        self.assertNotIn("Request governed action", html)

    def test_browser_preflight_evidence_is_owner_only_and_minimized(self):
        result = self._build()
        receipt = ui4.record_browser_preflight(self.root, result)
        self.assertTrue(receipt.path.is_file())
        value = json.loads(receipt.path.read_text(encoding="utf-8"))
        self.assertTrue(value["browser_preflight_post_observed"])
        self.assertFalse(value["organizational_authority_provided"])
        self.assertFalse(value["canonical_mutation_performed"])
        self.assertFalse(value["product_or_external_effect_performed"])
        self.assertFalse(value["reusable_secret_recorded"])
        self.assertFalse(value["browser_session_recorded"])
        serialized = json.dumps(value).lower()
        self.assertNotIn("credential", serialized)
        self.assertNotIn("cookie", serialized)
        self.assertNotIn("csrf", serialized)
        self.assertNotIn("session=", serialized)
        if os.name != "nt":
            self.assertEqual(stat.S_IMODE(receipt.path.stat().st_mode), 0o600)

    def test_run_form_rejects_authority_or_approval_inputs(self):
        body = f"preflight_id={ui4.PREFLIGHT_ID}&csrf=abc&organizational_authority=allow".encode()
        handler = SimpleNamespace(
            headers={"Content-Type": "application/x-www-form-urlencoded", "Content-Length": str(len(body))},
            rfile=io.BytesIO(body),
        )
        with self.assertRaises(ui4.UI4BoundaryError):
            ui4.read_run_form(handler)


if __name__ == "__main__":
    unittest.main()
