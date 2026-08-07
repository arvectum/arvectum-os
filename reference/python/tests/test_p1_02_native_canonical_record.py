from dataclasses import FrozenInstanceError
from datetime import datetime
import unittest

from arvectum_os_ref import ActorContext, Identity, OrganizationScope, Principal
from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord, build_p1_02_native_record


class P102NativeCanonicalRecordTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "principal-1", "platform"))
        self.actor = ActorContext(self.principal, self.organization)
        self.record = build_p1_02_native_record(
            organization=self.organization,
            actor=self.actor,
        )

    def test_first_native_version_has_stable_subject_and_distinct_version_identity(self) -> None:
        self.assertEqual(self.record.authority_mode, AuthorityMode.NATIVE)
        self.assertEqual(self.record.subject_id.value, "subject-1")
        self.assertEqual(self.record.version_id.value, "subject-1-v1")
        self.assertNotEqual(self.record.subject_id, self.record.version_id)
        self.assertEqual(self.record.subject_id.scope, "org-a")
        self.assertEqual(self.record.version_id.scope, "org-a")
        self.assertIsNone(self.record.predecessor_version_id)

    def test_record_carries_minimum_bounded_governed_envelope(self) -> None:
        self.assertEqual(self.record.organization, self.organization)
        self.assertEqual(self.record.creation_actor, self.actor)
        self.assertEqual(self.record.accountable_owner_id, self.principal.principal_id)
        self.assertTrue(self.record.semantic_type)
        self.assertTrue(self.record.schema_version)
        self.assertTrue(self.record.authority_scope)
        self.assertTrue(self.record.provenance_refs)
        self.assertTrue(self.record.integrity_metadata)
        self.assertIsNotNone(self.record.created_at.tzinfo)

    def test_published_value_object_is_immutable_in_memory(self) -> None:
        with self.assertRaises(FrozenInstanceError):
            self.record.version_id = Identity("canonical-version", "other", "org-a")  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            self.record.lifecycle_status = "changed"  # type: ignore[misc]

    def test_creation_actor_must_share_record_organization_scope(self) -> None:
        other_organization = OrganizationScope(Identity("organization", "org-b", "platform"))
        other_actor = ActorContext(self.principal, other_organization)

        with self.assertRaises(ValueError):
            CanonicalRecord(
                subject_id=self.record.subject_id,
                version_id=Identity("canonical-version", "subject-1-v2-invalid", "org-a"),
                semantic_type=self.record.semantic_type,
                schema_version=self.record.schema_version,
                organization=self.organization,
                authority_mode=AuthorityMode.NATIVE,
                authority_scope=self.record.authority_scope,
                accountable_owner_id=self.record.accountable_owner_id,
                creation_actor=other_actor,
                created_at=self.record.created_at,
                provenance_refs=self.record.provenance_refs,
                integrity_metadata=self.record.integrity_metadata,
            )

    def test_external_authority_modes_fail_closed_in_p1_02(self) -> None:
        for mode in (AuthorityMode.EXTERNAL_REFERENCE, AuthorityMode.GOVERNED_REPLICA):
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                CanonicalRecord(
                    subject_id=self.record.subject_id,
                    version_id=Identity("canonical-version", f"unsupported-{mode.name}", "org-a"),
                    semantic_type=self.record.semantic_type,
                    schema_version=self.record.schema_version,
                    organization=self.organization,
                    authority_mode=mode,
                    authority_scope=self.record.authority_scope,
                    accountable_owner_id=self.record.accountable_owner_id,
                    creation_actor=self.actor,
                    created_at=self.record.created_at,
                    provenance_refs=self.record.provenance_refs,
                    integrity_metadata=self.record.integrity_metadata,
                )

    def test_required_envelope_fields_fail_closed_when_missing_or_ambiguous(self) -> None:
        base = dict(
            subject_id=self.record.subject_id,
            version_id=Identity("canonical-version", "subject-1-v2-invalid", "org-a"),
            semantic_type=self.record.semantic_type,
            schema_version=self.record.schema_version,
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=self.record.authority_scope,
            accountable_owner_id=self.record.accountable_owner_id,
            creation_actor=self.actor,
            created_at=self.record.created_at,
            provenance_refs=self.record.provenance_refs,
            integrity_metadata=self.record.integrity_metadata,
        )

        for key, invalid_value in (
            ("semantic_type", ""),
            ("schema_version", ""),
            ("authority_scope", ""),
            ("provenance_refs", ()),
            ("integrity_metadata", ()),
            ("created_at", datetime(2026, 8, 7, 18, 50)),
        ):
            kwargs = dict(base)
            kwargs[key] = invalid_value
            with self.subTest(field=key), self.assertRaises(ValueError):
                CanonicalRecord(**kwargs)

    def test_identity_possession_does_not_create_permission_or_authority_state(self) -> None:
        self.assertFalse(hasattr(self.record.subject_id, "authorized"))
        self.assertFalse(hasattr(self.record, "authorization_granted"))
        self.assertFalse(hasattr(self.record, "organizational_authority"))


if __name__ == "__main__":
    unittest.main()
