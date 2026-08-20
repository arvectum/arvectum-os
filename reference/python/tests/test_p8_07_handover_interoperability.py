from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from p8_07_handover_interoperability import (
    FORMAT_VERSION,
    HandoverInteroperabilityError,
    PACKAGE_SCHEMA,
    PROOF_SCOPE,
    RECEIVER_KIND,
    create_governed_handover_package,
    validate_migration_authority_transition,
    verify_receiver_package,
)

RECEIVER_ID = "receiver:p8-07:isolated-proof"
SCRIPT = Path(__file__).parents[1] / "p8_07_handover_interoperability.py"


def rewrite_json(path: Path, mutate) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    mutate(value)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


class P807HandoverInteroperabilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def make_package(self) -> Path:
        package_dir = self.root / "handover"
        create_governed_handover_package(package_dir, receiver_id=RECEIVER_ID)
        return package_dir

    def test_package_preserves_identity_relationship_history_constraints_and_explicit_omissions(self) -> None:
        package_dir = self.make_package()
        package = json.loads((package_dir / "package.json").read_text(encoding="utf-8"))
        state = package["semantic_state"]
        handling = package["handling_constraints"]
        authority = package["authority"]

        self.assertEqual(package["schema"], PACKAGE_SCHEMA)
        self.assertEqual(package["format_version"], FORMAT_VERSION)
        self.assertEqual(package["scope"], PROOF_SCOPE)
        self.assertEqual(package["receiver"]["receiver_kind"], RECEIVER_KIND)
        self.assertEqual(state["subjects"][0]["subject_id"], state["versions"][0]["subject_id"])
        self.assertEqual(state["relationships"][0]["source"]["version_id"], state["versions"][0]["version_id"])
        self.assertTrue(any(item["kind"] == "secret" and item["reprovisioning"] for item in package["explicit_omissions"]))
        self.assertFalse(handling["rights"]["cross_organization_transfer"])
        self.assertTrue(handling["retention"]["receiver_must_preserve_constraint"])
        self.assertFalse(authority["external_transfer"]["activated"])
        self.assertFalse(authority["organizational_authority_transferred"])
        self.assertFalse(authority["technical_access_granted"])
        self.assertFalse(authority["credentials_exported"])

    def test_independent_receiver_process_validates_integrity_scope_and_reconstruction(self) -> None:
        package_dir = self.make_package()
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "verify",
                "--package-dir",
                str(package_dir),
                "--receiver-id",
                RECEIVER_ID,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr + completed.stdout)
        receipt = json.loads(completed.stdout)
        self.assertEqual(receipt["integrity"], "PASS")
        self.assertEqual(receipt["semantic_interpretation"], "PASS")
        self.assertEqual(receipt["handling_constraints_interpreted"], "PASS")
        self.assertEqual(receipt["historical_reconstruction"]["status"], "PASS")
        self.assertFalse(receipt["external_transfer_activated"])
        self.assertEqual(receipt["authority_transfer"], "NONE")
        self.assertEqual(receipt["technical_access_grant"], "NONE")

    def test_selected_historical_outcome_reconstructs_without_external_effect(self) -> None:
        package_dir = self.make_package()
        receipt = verify_receiver_package(package_dir, expected_receiver_id=RECEIVER_ID)
        self.assertEqual(receipt["historical_reconstruction"]["status"], "PASS")
        self.assertEqual(receipt["external_effect_replay"], "DENIED")

    def test_tampered_payload_fails_closed(self) -> None:
        package_dir = self.make_package()
        rewrite_json(
            package_dir / "package.json",
            lambda value: value["handling_constraints"]["rights"].__setitem__("redistribute", True),
        )
        with self.assertRaisesRegex(HandoverInteroperabilityError, "package integrity mismatch"):
            verify_receiver_package(package_dir, expected_receiver_id=RECEIVER_ID)

    def test_tampered_manifest_or_unsupported_version_fails_closed(self) -> None:
        package_dir = self.make_package()
        package_path = package_dir / "package.json"
        rewrite_json(package_path, lambda value: value.__setitem__("format_version", "999"))
        (package_dir / "package.sha256").write_text(
            __import__("hashlib").sha256(package_path.read_bytes()).hexdigest() + "\n", encoding="utf-8"
        )
        with self.assertRaisesRegex(HandoverInteroperabilityError, "unsupported format version"):
            verify_receiver_package(package_dir, expected_receiver_id=RECEIVER_ID)

    def test_receiver_scope_mismatch_fails_closed(self) -> None:
        package_dir = self.make_package()
        with self.assertRaisesRegex(HandoverInteroperabilityError, "receiver mismatch"):
            verify_receiver_package(package_dir, expected_receiver_id="receiver:wrong")

    def test_external_transfer_activation_is_unavailable_without_fresh_governed_implementation(self) -> None:
        with self.assertRaisesRegex(HandoverInteroperabilityError, "outside the current P8.07 proof"):
            create_governed_handover_package(
                self.root / "external",
                receiver_id=RECEIVER_ID,
                external_transfer_activated=True,
            )

    def test_dual_authority_migration_fails_closed(self) -> None:
        with self.assertRaisesRegex(HandoverInteroperabilityError, "two concurrently authoritative systems"):
            validate_migration_authority_transition(
                source_authority_active=True,
                receiver_authority_active=True,
                transition_authorization_ref="transition:even-explicit-cannot-be-dual-active",
            )

    def test_receiver_authority_without_governed_transition_fails_closed(self) -> None:
        with self.assertRaisesRegex(HandoverInteroperabilityError, "explicit governed transition authorization"):
            validate_migration_authority_transition(
                source_authority_active=False,
                receiver_authority_active=True,
                transition_authorization_ref=None,
            )

    def test_secret_dependency_is_omitted_and_reprovisioned_separately(self) -> None:
        package_dir = self.make_package()
        all_bytes = (package_dir / "package.json").read_bytes()
        self.assertNotIn(b'"secret_value"', all_bytes.lower())
        self.assertNotIn(b'"credential_value"', all_bytes.lower())
        package = json.loads(all_bytes)
        secret = next(item for item in package["explicit_omissions"] if item["kind"] == "secret")
        self.assertIn("separate authorized channel", secret["reprovisioning"])

    def test_termination_and_revocation_path_is_explicit(self) -> None:
        package_dir = self.make_package()
        package = json.loads((package_dir / "package.json").read_text(encoding="utf-8"))
        controls = package["termination_and_revocation"]
        self.assertTrue(controls["active_credentials_must_be_revoked_separately"])
        self.assertTrue(controls["receiver_access_must_be_revoked_separately"])
        self.assertTrue(controls["post_termination_retention_or_deletion_instruction_required"])
        self.assertTrue(controls["handover_or_deletion_evidence_required_where_applicable"])


if __name__ == "__main__":
    unittest.main()
