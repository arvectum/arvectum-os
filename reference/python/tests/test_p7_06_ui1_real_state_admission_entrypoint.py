import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from arvectum_os_ref.canonical import AuthorityMode
import p7_03_durable_state as p703
import p7_06_ui1_real_state_admission as admission
import p7_06_ui1_real_state_admission_entrypoint as entrypoint


class P706UI1RealStateAdmissionEntrypointTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "runtime"
        self.release_sha = "b" * 40
        p703.initialize_store(self.root, self.release_sha)
        self.subject = "document-subject/eis-test@org"
        self.version = "document-version/eis-test-v1@org"

    def tearDown(self):
        self.tmp.cleanup()

    def _metadata(self, **overrides):
        value = {
            "state_class": "canonical-governed-state",
            "organization_scope": p703.ORGANIZATION_SCOPE,
            "semantic_type": "platform.document",
            "schema_version": "p7.06-ui1-real-eis-evidence-1",
            "classification": admission.PERSISTED_CLASSIFICATION,
            "retention_policy_ref": admission.PERSISTED_RETENTION,
            "source_release_sha": self.release_sha,
            "subject_identity": self.subject,
            "version_identity": self.version,
            "authority_mode": AuthorityMode.EXTERNAL_REFERENCE.value,
            "authority_scope": admission.DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
            "authoritative_source": admission.EXTERNAL_SOURCE_AUTHORITY,
            "validation_status": entrypoint.EXPECTED_VALIDATION_STATUS,
            "governed_admission_ref": "event-version/admission-v1@org",
            "provenance_refs": [
                "principal/owner@org",
                "execution-subject/run@org",
                "execution-version/run-v5@org",
                "event-subject/admission@org",
                "event-version/admission-v1@org",
            ],
            "source_manifest_sha256": admission.APPROVED_MANIFEST_SHA256,
            "product_contract_version": "0.1.0",
            "canonical_authority": True,
            "contains_reusable_secret": False,
            "raw_document_bytes_included": False,
            "external_actions": False,
        }
        value.update(overrides)
        return value

    def _persist(self, metadata):
        return p703.persist_governed_item(
            self.root,
            self.release_sha,
            json.dumps({"safe": True}).encode("utf-8"),
            metadata,
        )

    def test_no_existing_exact_item_returns_none(self):
        self.assertIsNone(
            entrypoint.verify_existing_retry_semantics(
                self.root,
                subject_identity=self.subject,
                version_identity=self.version,
            )
        )

    def test_exact_valid_retained_item_is_accepted(self):
        item_id = self._persist(self._metadata())
        self.assertEqual(
            entrypoint.verify_existing_retry_semantics(
                self.root,
                subject_identity=self.subject,
                version_identity=self.version,
            ),
            item_id,
        )

    def test_matching_subject_version_with_incomplete_validation_fails_closed(self):
        self._persist(self._metadata(validation_status="CAP-001 admitted only"))
        with self.assertRaisesRegex(
            entrypoint.UI1RealStateEntrypointError,
            "validation_status",
        ):
            entrypoint.verify_existing_retry_semantics(
                self.root,
                subject_identity=self.subject,
                version_identity=self.version,
            )

    def test_matching_subject_version_with_semantic_source_or_contract_drift_fails_closed(self):
        for key, bad in (
            ("semantic_type", "platform.event"),
            ("schema_version", "different-schema"),
            ("authoritative_source", "unknown"),
            ("source_manifest_sha256", "0" * 64),
            ("product_contract_version", "0.2.0"),
            ("authority_mode", AuthorityMode.NATIVE.value),
        ):
            with self.subTest(key=key):
                root = Path(self.tmp.name) / f"runtime-{key}"
                p703.initialize_store(root, self.release_sha)
                p703.persist_governed_item(
                    root,
                    self.release_sha,
                    b"safe",
                    self._metadata(**{key: bad}),
                )
                with self.assertRaises(entrypoint.UI1RealStateEntrypointError):
                    entrypoint.verify_existing_retry_semantics(
                        root,
                        subject_identity=self.subject,
                        version_identity=self.version,
                    )

    def test_entrypoint_rejects_additional_minimization_drift_allowed_by_p703(self):
        for key in ("raw_document_bytes_included", "external_actions"):
            with self.subTest(key=key):
                root = Path(self.tmp.name) / f"runtime-{key}"
                p703.initialize_store(root, self.release_sha)
                p703.persist_governed_item(
                    root,
                    self.release_sha,
                    b"safe",
                    self._metadata(**{key: True}),
                )
                with self.assertRaises(entrypoint.UI1RealStateEntrypointError):
                    entrypoint.verify_existing_retry_semantics(
                        root,
                        subject_identity=self.subject,
                        version_identity=self.version,
                    )

    def test_p703_itself_rejects_core_canonical_secret_and_integrity_drift(self):
        for overrides in (
            {"canonical_authority": False},
            {"contains_reusable_secret": True},
            {"governed_admission_ref": ""},
            {"source_release_sha": "short"},
        ):
            root = Path(self.tmp.name) / f"p703-{len(tuple(Path(self.tmp.name).iterdir()))}"
            p703.initialize_store(root, self.release_sha)
            with self.assertRaises(p703.BoundaryError):
                p703.persist_governed_item(
                    root,
                    self.release_sha,
                    b"safe",
                    self._metadata(**overrides),
                )

    def test_matching_subject_version_with_bounded_but_incomplete_provenance_fails_closed(self):
        root = Path(self.tmp.name) / "runtime-short-provenance"
        p703.initialize_store(root, self.release_sha)
        p703.persist_governed_item(
            root,
            self.release_sha,
            b"safe",
            self._metadata(provenance_refs=["one-valid-ref"]),
        )
        with self.assertRaisesRegex(entrypoint.UI1RealStateEntrypointError, "provenance"):
            entrypoint.verify_existing_retry_semantics(
                root,
                subject_identity=self.subject,
                version_identity=self.version,
            )

    def test_duplicate_exact_subject_version_fails_closed(self):
        self._persist(self._metadata())
        p703.persist_governed_item(
            self.root,
            self.release_sha,
            b"safe-2",
            self._metadata(governed_admission_ref="event-version/admission-v2@org"),
        )
        with self.assertRaisesRegex(entrypoint.UI1RealStateEntrypointError, "multiple"):
            entrypoint.verify_existing_retry_semantics(
                self.root,
                subject_identity=self.subject,
                version_identity=self.version,
            )

    def test_selected_mac_entrypoint_checks_existing_semantics_before_base_run(self):
        bad_metadata = self._metadata(validation_status="incomplete")
        self._persist(bad_metadata)
        fake_connection = type(
            "Conn",
            (),
            {
                "organization_scope": type("OrgScope", (), {"organization_id": "org"})(),
                "principal": type("Principal", (), {"principal_id": "principal"})(),
            },
        )()
        with patch.object(
            admission,
            "_verify_exact_release",
            return_value=(self.release_sha, Path(self.tmp.name)),
        ), patch.object(
            admission,
            "_authorize_operator",
            return_value=("org", "principal", object()),
        ), patch.object(
            admission,
            "connect_product",
            return_value=(0, (), fake_connection),
        ), patch.object(
            admission,
            "_target_identity_pair",
            return_value=(self.subject, self.version),
        ), patch.object(admission, "run_admission") as base_run:
            with self.assertRaises(entrypoint.UI1RealStateEntrypointError):
                entrypoint.run_selected_mac_admission(
                    runtime_root=self.root,
                    access_root=Path(self.tmp.name),
                    state_file=Path(self.tmp.name) / "state.json",
                    credential_id="credential",
                    credential_file=Path(self.tmp.name) / "credential",
                    l7_manifest=Path(self.tmp.name) / "manifest.json",
                    owner_approval=admission.OWNER_APPROVAL_ASSERTION,
                )
        base_run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
