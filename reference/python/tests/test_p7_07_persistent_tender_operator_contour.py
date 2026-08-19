import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from arvectum_os_ref.identity import Identity
import p7_03_durable_state as p703
import p7_04_persistent_access as p704
import p7_07_persistent_tender_operator_contour as p707


class DelegatingProductBridge:
    def __init__(self, adapters):
        self.adapters = adapters
        self.calls = 0

    def resolve_document(self, **kwargs):
        self.calls += 1
        return self.adapters.capabilities.resolve_document(**kwargs)


class P707PersistentTenderOperatorContourTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.runtime_root = self.base / "runtime"
        self.access_root = self.base / "access"
        self.context_dir = self.base / "context"
        self.context_dir.mkdir(mode=0o700)
        self.state_file = self.context_dir / "organization-operator.json"
        self.org = Identity("organization", "p7-07-org", "platform")
        self.human = Identity("principal", "p7-07-owner", self.org.value)
        self.release_sha = "b" * 40
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
            "schema_version": p707.MANIFEST_SCHEMA,
            "purpose": p707.MANIFEST_PURPOSE,
            "status": p707.MANIFEST_STATUS,
            "notice_number": p707.NOTICE_NUMBER,
            "expected_document_count": 7,
            "exact_document_count": 7,
            "missing_names": [],
            "duplicate_names": [],
            "external_actions": False,
            "external_source_authority": p707.EXTERNAL_SOURCE_AUTHORITY,
            "external_source_reference": f"44fz-notice:{p707.NOTICE_NUMBER}",
            "external_source_version": "test-p7-07-safe-ref-v1",
            "retrieved_at": "2026-08-18T12:00:00+00:00",
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

    def _setup(self):
        path, digest = self._manifest()
        with patch.object(p707, "APPROVED_MANIFEST_SHA256", digest), patch.object(
            p707, "_verify_exact_release", return_value=(self.release_sha, self.repo_root)
        ):
            result = p707.run_setup(
                runtime_root=self.runtime_root,
                access_root=self.access_root,
                state_file=self.state_file,
                credential_id=self.credential["credential_id"],
                credential_file=self.credential_file,
                l7_manifest=path,
                owner_approval=p707.OWNER_APPROVAL_ASSERTION,
                evidence_output=self.base / "setup-evidence.json",
            )
        return result, path, digest

    def test_manifest_verification_recomputes_body_hash(self):
        path, digest = self._manifest()
        with patch.object(p707, "APPROVED_MANIFEST_SHA256", digest):
            verified = p707.load_verified_manifest(path)
        self.assertEqual(verified.manifest_sha256, digest)
        value = json.loads(path.read_text(encoding="utf-8"))
        value["documents"][0]["size_bytes"] += 1
        path.write_text(json.dumps(value), encoding="utf-8")
        if os.name != "nt":
            path.chmod(0o600)
        with patch.object(p707, "APPROVED_MANIFEST_SHA256", digest):
            with self.assertRaises(p707.P707Error):
                p707.load_verified_manifest(path)

    def test_setup_admits_rehydratable_prebid_review_document_and_narrows_access(self):
        result, _path, digest = self._setup()
        self.assertEqual(result.status, "PASS_ADMITTED_AND_CONFIGURED")
        self.assertFalse(result.idempotent_existing_item)
        self.assertTrue(result.reconstruction_complete)
        store = p703.verify_store(self.runtime_root)
        self.assertEqual(store["governed_items"], 1)
        self.assertEqual(store["checkpoints"], 1)

        item_dir = self.runtime_root / "state" / "governed" / "items" / result.storage_item_id
        manifest = p703.verify_item(item_dir)
        metadata = manifest["metadata"]
        self.assertEqual(metadata["operational_contour"], "P7.07")
        self.assertTrue(metadata["rehydratable_cap001_document"])
        self.assertEqual(metadata["source_manifest_sha256"], digest)
        self.assertEqual(metadata["product_contract_version"], "0.1.0")
        self.assertEqual(metadata["authoritative_source"], p707.EXTERNAL_SOURCE_AUTHORITY)
        self.assertFalse(metadata["raw_document_bytes_included"])
        self.assertFalse(metadata["external_actions"])

        config = p707._load_config(self.runtime_root)
        self.assertEqual(config["storage_item_id"], result.storage_item_id)
        self.assertEqual(config["read_operation"], p707.OP_RESOLVE_DOCUMENT)

        state = p704.load_access_store(self.access_root)
        active_setup = [
            grant for grant in state["grants"].values()
            if grant["status"] == "active" and grant["operation"] == p707.SETUP_ACCESS_OPERATION
        ]
        active_read = [
            grant for grant in state["grants"].values()
            if grant["status"] == "active"
            and grant["operation"] == p707.READ_ACCESS_OPERATION
            and grant["resource"] == config["read_resource"]
        ]
        self.assertEqual(active_setup, [])
        self.assertEqual(len(active_read), 1)

        with patch.object(p707, "APPROVED_MANIFEST_SHA256", digest), patch.object(
            p707, "_verify_exact_release", return_value=(self.release_sha, self.repo_root)
        ):
            rc, _lines, connection = p707.connect_product(self.state_file, arvectum_repo_root=self.repo_root)
            self.assertEqual(rc, 0)
            _metadata, payload = p707._read_item_payload(self.runtime_root, result.storage_item_id)
            admitted = p707._rehydrate_admitted(payload, connection=connection)
        artifact = admitted.artifacts[0]
        self.assertEqual(artifact.handling.purpose, "prebid-review")
        self.assertEqual(artifact.handling.rights, ("read",))
        self.assertEqual(artifact.handling.classification, "restricted-pilot")
        self.assertEqual(artifact.integrity_ref, f"sha256:{digest}")
        self.assertEqual(admitted.canonical_record.authority_mode.value, "External Reference")
        self.assertEqual(
            admitted.canonical_record.external_authority.authoritative_system,
            p707.EXTERNAL_SOURCE_AUTHORITY,
        )

    def test_setup_retry_is_idempotent_for_canonical_item_and_checkpoint(self):
        first, path, digest = self._setup()
        after_first = p703.verify_store(self.runtime_root)
        with patch.object(p707, "APPROVED_MANIFEST_SHA256", digest), patch.object(
            p707, "_verify_exact_release", return_value=(self.release_sha, self.repo_root)
        ):
            second = p707.run_setup(
                runtime_root=self.runtime_root,
                access_root=self.access_root,
                state_file=self.state_file,
                credential_id=self.credential["credential_id"],
                credential_file=self.credential_file,
                l7_manifest=path,
                owner_approval=p707.OWNER_APPROVAL_ASSERTION,
                evidence_output=self.base / "setup-evidence-2.json",
            )
        after_second = p703.verify_store(self.runtime_root)
        self.assertEqual(first.storage_item_id, second.storage_item_id)
        self.assertEqual(second.status, "PASS_IDEMPOTENT_EXISTING")
        self.assertTrue(second.idempotent_existing_item)
        self.assertEqual(after_first["governed_items"], after_second["governed_items"])
        self.assertEqual(after_first["checkpoints"], after_second["checkpoints"])
        self.assertEqual(after_second["governed_items"], 1)
        self.assertEqual(after_second["checkpoints"], 1)

    def test_consume_uses_product_bridge_cap001_and_is_state_read_only(self):
        setup, _path, digest = self._setup()
        before = self._state_digest()
        created = []

        def bridge_loader(_repo, adapters):
            bridge = DelegatingProductBridge(adapters)
            created.append(bridge)
            return bridge, "f" * 64

        with patch.object(p707, "APPROVED_MANIFEST_SHA256", digest), patch.object(
            p707, "_verify_exact_release", return_value=(self.release_sha, self.repo_root)
        ), patch.object(p707, "_load_product_bridge", side_effect=bridge_loader):
            result = p707.run_consume(
                runtime_root=self.runtime_root,
                access_root=self.access_root,
                state_file=self.state_file,
                credential_id=self.credential["credential_id"],
                credential_file=self.credential_file,
                product_repo=self.base / "product",
                evidence_output=self.base / "consume-evidence.json",
            )
        self.assertEqual(result.status, "PASS_EXACT_CAP001_RELIANCE")
        self.assertEqual(result.storage_item_id, setup.storage_item_id)
        self.assertEqual(result.integrity_ref, f"sha256:{digest}")
        self.assertEqual(result.authoritative_source, p707.EXTERNAL_SOURCE_AUTHORITY)
        self.assertEqual(result.product_contract_version, "0.1.0")
        self.assertEqual(len(created), 1)
        self.assertEqual(created[0].calls, 1)
        self.assertEqual(before, self._state_digest())

    def test_read_grant_revocation_blocks_before_product_bridge(self):
        _setup, _path, digest = self._setup()
        state = p704.load_access_store(self.access_root)
        read_gid = next(
            gid for gid, grant in state["grants"].items()
            if grant["status"] == "active" and grant["operation"] == p707.READ_ACCESS_OPERATION
        )
        p704.revoke_grant(self.access_root, read_gid)
        with patch.object(p707, "APPROVED_MANIFEST_SHA256", digest), patch.object(
            p707, "_verify_exact_release", return_value=(self.release_sha, self.repo_root)
        ), patch.object(p707, "_load_product_bridge") as bridge_loader:
            with self.assertRaisesRegex(p707.P707Error, "P7.04 authorization denied"):
                p707.run_consume(
                    runtime_root=self.runtime_root,
                    access_root=self.access_root,
                    state_file=self.state_file,
                    credential_id=self.credential["credential_id"],
                    credential_file=self.credential_file,
                    product_repo=self.base / "product",
                )
        bridge_loader.assert_not_called()

    def test_wrong_owner_assertion_blocks_before_access_or_state_change(self):
        path, digest = self._manifest()
        before = self._state_digest()
        with patch.object(p707, "APPROVED_MANIFEST_SHA256", digest), patch.object(
            p707, "_verify_exact_release"
        ) as release_check:
            with self.assertRaises(p707.P707Error):
                p707.run_setup(
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
        state = p704.load_access_store(self.access_root)
        self.assertEqual(state["grants"], {})

    def test_operational_source_has_no_network_process_or_eis_adapter(self):
        source = Path(p707.__file__).read_text(encoding="utf-8")
        forbidden = (
            "import socket",
            "from socket",
            "import requests",
            "from requests",
            "urllib.request",
            "subprocess.",
            "getDocsIP(",
            "send_email(",
            "send_telegram(",
            "digital_signature(",
        )
        for token in forbidden:
            self.assertNotIn(token, source)
        self.assertIn('"external_actions": False', source)
        self.assertIn('"raw_document_bytes_included": False', source)
        self.assertIn("ArvectumOSBridge", source)


if __name__ == "__main__":
    unittest.main()
