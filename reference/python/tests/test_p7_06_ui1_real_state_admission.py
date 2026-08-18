import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from arvectum_os_ref.canonical import AuthorityMode
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.governed_execution import GovernedGateKind
import p7_03_durable_state as p703
import p7_04_persistent_access as p704
import p7_06_ui1_real_state_admission as admission


class P706UI1RealStateAdmissionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.runtime_root = self.base / "runtime"
        self.access_root = self.base / "access"
        self.context_dir = self.base / "context"
        self.context_dir.mkdir(mode=0o700)
        self.state_file = self.context_dir / "organization-operator.json"
        self.org = Identity("organization", "p7-ui1-real-org", "platform")
        self.human = Identity("principal", "p7-ui1-real-owner", self.org.value)
        self.release_sha = "a" * 40
        self.repo_root = Path(__file__).resolve().parents[3]
        self._write_context()
        p704.initialize_access_store(self.access_root, self.org)
        p704.register_principal(self.access_root, self.human, kind="human")
        self.credential = p704.issue_credential(self.access_root, self.human)
        self.credential_file = Path(self.credential["secret_path"])
        p703.initialize_store(self.runtime_root, self.release_sha)

    def tearDown(self):
        self.tmp.cleanup()

    def _write_context(self):
        payload = {
            "schema_version": "p6.05-l4-local-context-1",
            "organization": {
                "identity": {"namespace": "organization", "value": self.org.value, "scope": "platform"},
                "context_label": "ООО «Арвектум»",
            },
            "operator": {
                "identity": {"namespace": "principal", "value": self.human.value, "scope": self.org.value},
                "principal_category": "human",
                "operating_mode": "owner-operated",
            },
            "authority": {
                "authorization_grants": [],
                "delegations": [],
                "organizational_authority_claimed": False,
            },
            "authentication": {"evidence_refs": []},
            "bootstrap": {"scope": "P6.05-L4", "owner_authorization_asserted": True},
        }
        self.state_file.write_text(json.dumps(payload), encoding="utf-8")
        if os.name != "nt":
            self.state_file.chmod(0o600)

    @staticmethod
    def _canonical_bytes(value):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")

    def _manifest(self):
        body = {
            "schema_version": admission.MANIFEST_SCHEMA,
            "purpose": admission.MANIFEST_PURPOSE,
            "status": admission.MANIFEST_STATUS,
            "notice_number": admission.NOTICE_NUMBER,
            "expected_document_count": 7,
            "exact_document_count": 7,
            "missing_names": [],
            "duplicate_names": [],
            "external_actions": False,
            "external_source_authority": admission.EXTERNAL_SOURCE_AUTHORITY,
            "external_source_reference": f"44fz-notice:{admission.NOTICE_NUMBER}",
            "external_source_version": "test-safe-ref-v1",
            "retrieved_at": "2026-08-15T12:00:00+00:00",
            "documents": [
                {"index": index, "sha256": f"{index:064x}", "size_bytes": index * 10}
                for index in range(1, 8)
            ],
        }
        digest = hashlib.sha256(self._canonical_bytes(body)).hexdigest()
        value = {
            **body,
            "manifest_sha256": digest,
            "manifest_integrity_ref": f"sha256:{digest}",
        }
        path = self.base / "retained-manifest.json"
        path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2), encoding="utf-8")
        if os.name != "nt":
            path.chmod(0o600)
        return path, digest

    def _grant(self):
        return p704.grant_access(
            self.access_root,
            self.human,
            operation=admission.ACCESS_OPERATION,
            resource=admission.ACCESS_RESOURCE,
            access_paths=(admission.ACCESS_PATH,),
        )

    def _run(self, manifest_path, digest, *, evidence_name="evidence.json"):
        self._grant()
        evidence = self.base / evidence_name
        with patch.object(admission, "APPROVED_MANIFEST_SHA256", digest), patch.object(
            admission,
            "_verify_exact_release",
            return_value=(self.release_sha, self.repo_root),
        ):
            result = admission.run_admission(
                runtime_root=self.runtime_root,
                access_root=self.access_root,
                state_file=self.state_file,
                credential_id=self.credential["credential_id"],
                credential_file=self.credential_file,
                l7_manifest=manifest_path,
                owner_approval=admission.OWNER_APPROVAL_ASSERTION,
                evidence_output=evidence,
            )
        return result, evidence

    def _state_digest(self):
        digest = hashlib.sha256()
        state = self.runtime_root / "state"
        for path in sorted(item for item in state.rglob("*") if item.is_file()):
            rel = path.relative_to(state).as_posix().encode()
            data = path.read_bytes()
            digest.update(rel)
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
        return digest.hexdigest()

    def test_manifest_verification_recomputes_canonical_body_hash(self):
        path, digest = self._manifest()
        with patch.object(admission, "APPROVED_MANIFEST_SHA256", digest):
            verified = admission.load_verified_manifest(path)
        self.assertEqual(verified.manifest_sha256, digest)
        self.assertEqual(verified.source_version, "test-safe-ref-v1")

        value = json.loads(path.read_text(encoding="utf-8"))
        value["documents"][0]["size_bytes"] += 1
        path.write_text(json.dumps(value), encoding="utf-8")
        if os.name != "nt":
            path.chmod(0o600)
        with patch.object(admission, "APPROVED_MANIFEST_SHA256", digest):
            with self.assertRaises(admission.UI1RealStateAdmissionError):
                admission.load_verified_manifest(path)

    def test_wrong_owner_assertion_blocks_before_exact_release_or_state_write(self):
        path, digest = self._manifest()
        before = self._state_digest()
        with patch.object(admission, "APPROVED_MANIFEST_SHA256", digest), patch.object(
            admission, "_verify_exact_release"
        ) as release_check:
            with self.assertRaises(admission.UI1RealStateAdmissionError):
                admission.run_admission(
                    runtime_root=self.runtime_root,
                    access_root=self.access_root,
                    state_file=self.state_file,
                    credential_id=self.credential["credential_id"],
                    credential_file=self.credential_file,
                    l7_manifest=path,
                    owner_approval="NOT_APPROVED",
                )
        release_check.assert_not_called()
        self.assertEqual(before, self._state_digest())

    def test_missing_exact_p704_grant_blocks_before_manifest_read_and_p703_write(self):
        before = self._state_digest()
        missing_manifest = self.base / "must-not-be-read.json"
        with patch.object(
            admission,
            "_verify_exact_release",
            return_value=(self.release_sha, self.repo_root),
        ):
            with self.assertRaisesRegex(admission.UI1RealStateAdmissionError, "P7.04 authorization denied"):
                admission.run_admission(
                    runtime_root=self.runtime_root,
                    access_root=self.access_root,
                    state_file=self.state_file,
                    credential_id=self.credential["credential_id"],
                    credential_file=self.credential_file,
                    l7_manifest=missing_manifest,
                    owner_approval=admission.OWNER_APPROVAL_ASSERTION,
                )
        self.assertFalse(missing_manifest.exists())
        self.assertEqual(before, self._state_digest())

    def test_four_required_gate_bases_are_distinct_and_scoped(self):
        values = {
            kind: admission._gate_basis(kind, self.org.value)
            for kind in (
                GovernedGateKind.AUTHORIZATION,
                GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
                GovernedGateKind.DATA_GOVERNANCE,
                GovernedGateKind.CONSEQUENTIAL_APPROVAL,
            )
        }
        self.assertEqual(len(set(values.values())), 4)
        self.assertTrue(all(value.scope == self.org.value for value in values.values()))
        self.assertNotEqual(
            values[GovernedGateKind.AUTHORIZATION],
            values[GovernedGateKind.ORGANIZATIONAL_AUTHORITY],
        )
        self.assertNotEqual(
            values[GovernedGateKind.DATA_GOVERNANCE],
            values[GovernedGateKind.CONSEQUENTIAL_APPROVAL],
        )

    def test_end_to_end_real_state_bridge_admits_external_reference_and_persists_minimized_item(self):
        path, digest = self._manifest()
        result, evidence_path = self._run(path, digest)
        self.assertEqual(result.status, "PASS_ADMITTED_AND_PERSISTED")
        self.assertFalse(result.idempotent_existing_item)
        self.assertTrue(result.reconstruction_complete)
        self.assertIsNotNone(result.checkpoint_id)

        store = p703.verify_store(self.runtime_root)
        self.assertEqual(store["governed_items"], 1)
        self.assertEqual(store["checkpoints"], 1)
        item_dir = self.runtime_root / "state" / "governed" / "items" / result.storage_item_id
        item = p703.verify_item(item_dir)
        metadata = item["metadata"]
        self.assertEqual(metadata["state_class"], "canonical-governed-state")
        self.assertEqual(metadata["authority_mode"], AuthorityMode.EXTERNAL_REFERENCE.value)
        self.assertEqual(metadata["authoritative_source"], admission.EXTERNAL_SOURCE_AUTHORITY)
        self.assertEqual(metadata["source_manifest_sha256"], digest)
        self.assertTrue(metadata["canonical_authority"])
        self.assertFalse(metadata["contains_reusable_secret"])
        self.assertFalse(metadata["raw_document_bytes_included"])
        self.assertFalse(metadata["external_actions"])
        self.assertNotEqual(metadata["subject_identity"], metadata["version_identity"])
        self.assertGreaterEqual(len(metadata["provenance_refs"]), 5)

        payload = json.loads((item_dir / "payload.bin").read_text(encoding="utf-8"))
        self.assertEqual(payload["manifest_sha256"], digest)
        self.assertFalse(payload["raw_document_bytes_included"])
        self.assertFalse(payload["external_actions"])
        self.assertFalse(payload["reusable_secret_included"])
        self.assertNotIn("documents", payload)

        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        self.assertEqual(evidence["status"], "PASS_ADMITTED_AND_PERSISTED")
        self.assertTrue(evidence["all_required_gates_allow"])
        self.assertFalse(evidence["p7_04_authorization"]["organizational_authority_satisfied"])
        self.assertFalse(evidence["p7_04_authorization"]["consequential_approval_satisfied"])
        self.assertFalse(evidence["network_invoked"])
        self.assertFalse(evidence["external_actions"])
        self.assertFalse(evidence["credential_secret_exposed"])
        self.assertNotIn(self.credential["credential_id"], evidence_path.read_text(encoding="utf-8"))
        secret = p704.read_credential_secret(self.credential_file)
        self.assertNotIn(secret, evidence_path.read_text(encoding="utf-8"))

    def test_retry_is_idempotent_and_does_not_create_second_item_or_checkpoint(self):
        path, digest = self._manifest()
        first, _ = self._run(path, digest, evidence_name="first.json")
        state_after_first = p703.verify_store(self.runtime_root)
        second, _ = self._run(path, digest, evidence_name="second.json")
        state_after_second = p703.verify_store(self.runtime_root)
        self.assertEqual(first.storage_item_id, second.storage_item_id)
        self.assertTrue(second.idempotent_existing_item)
        self.assertEqual(second.status, "PASS_IDEMPOTENT_EXISTING")
        self.assertEqual(state_after_first["governed_items"], state_after_second["governed_items"])
        self.assertEqual(state_after_first["checkpoints"], state_after_second["checkpoints"])
        self.assertEqual(state_after_second["governed_items"], 1)
        self.assertEqual(state_after_second["checkpoints"], 1)

    def test_conflicting_exact_subject_version_retained_state_fails_closed(self):
        path, digest = self._manifest()
        self._grant()
        with patch.object(admission, "APPROVED_MANIFEST_SHA256", digest):
            rc, _lines, connection = admission.connect_product(
                self.state_file,
                arvectum_repo_root=self.repo_root,
            )
            self.assertEqual(rc, 0)
            subject, version = admission._target_identity_pair(connection)
        bad_metadata = {
            "state_class": "canonical-governed-state",
            "organization_scope": p703.ORGANIZATION_SCOPE,
            "semantic_type": "platform.document",
            "schema_version": "p7.06-ui1-real-eis-evidence-1",
            "classification": admission.PERSISTED_CLASSIFICATION,
            "retention_policy_ref": admission.PERSISTED_RETENTION,
            "source_release_sha": self.release_sha,
            "subject_identity": subject,
            "version_identity": version,
            "authority_mode": AuthorityMode.EXTERNAL_REFERENCE.value,
            "authority_scope": "platform.document/external-evidence",
            "governed_admission_ref": "conflicting-admission",
            "provenance_refs": ["conflicting-provenance"],
            "source_manifest_sha256": "0" * 64,
            "canonical_authority": True,
            "contains_reusable_secret": False,
        }
        p703.persist_governed_item(self.runtime_root, self.release_sha, b"conflicting", bad_metadata)
        before = p703.verify_store(self.runtime_root)["governed_items"]
        with patch.object(admission, "APPROVED_MANIFEST_SHA256", digest), patch.object(
            admission,
            "_verify_exact_release",
            return_value=(self.release_sha, self.repo_root),
        ):
            with self.assertRaisesRegex(admission.UI1RealStateAdmissionError, "conflicts with approved source manifest"):
                admission.run_admission(
                    runtime_root=self.runtime_root,
                    access_root=self.access_root,
                    state_file=self.state_file,
                    credential_id=self.credential["credential_id"],
                    credential_file=self.credential_file,
                    l7_manifest=path,
                    owner_approval=admission.OWNER_APPROVAL_ASSERTION,
                )
        self.assertEqual(p703.verify_store(self.runtime_root)["governed_items"], before)

    def test_source_has_no_network_or_external_effect_adapter(self):
        source = Path(admission.__file__).read_text(encoding="utf-8")
        forbidden = (
            "import socket",
            "from socket",
            "import requests",
            "from requests",
            "urllib.request",
            "subprocess.",
            "getDocsIP",
            "send_email",
            "send_telegram",
            "digital_signature",
        )
        for token in forbidden:
            self.assertNotIn(token, source)
        self.assertIn('"external_actions": False', source)
        self.assertIn('"raw_document_bytes_included": False', source)


if __name__ == "__main__":
    unittest.main()
