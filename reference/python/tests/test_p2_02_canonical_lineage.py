from dataclasses import replace
from datetime import datetime
import unittest

from arvectum_os_ref.canonical import CanonicalRecord
from arvectum_os_ref.canonical_lineage import (
    AmbiguousEffectiveVersionError,
    CanonicalLineage,
    CanonicalLineageConflictError,
    CanonicalVersionNotFoundError,
    NoEffectiveVersionError,
)
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.reference_scenario import build_p1_reference_scenario


def at(value: str) -> datetime:
    return datetime.fromisoformat(value)


class P202CanonicalLineageTests(unittest.TestCase):
    def setUp(self) -> None:
        scenario = build_p1_reference_scenario()
        base = scenario.input_record
        boundary_2 = at("2026-09-01T00:00:00+00:00")
        boundary_3 = at("2026-10-01T00:00:00+00:00")

        self.v1 = replace(
            base,
            effective_from=at("2026-08-01T00:00:00+00:00"),
            effective_until=boundary_2,
        )
        self.v2 = replace(
            base,
            version_id=Identity(
                "canonical-version",
                "subject-1-v2-lineage",
                base.organization.organization_id.value,
            ),
            created_at=at("2026-08-08T00:00:00+00:00"),
            predecessor_version_id=self.v1.version_id,
            payload=(("label", "scheduled successor"),),
            effective_from=boundary_2,
            effective_until=boundary_3,
        )
        self.v3 = replace(
            base,
            version_id=Identity(
                "canonical-version",
                "subject-1-v3-lineage",
                base.organization.organization_id.value,
            ),
            created_at=at("2026-08-09T00:00:00+00:00"),
            predecessor_version_id=self.v2.version_id,
            payload=(("label", "later scheduled successor"),),
            effective_from=boundary_3,
            effective_until=None,
        )
        # Input order is intentionally non-lineage order. Resolution must come
        # from immutable predecessor semantics rather than collection order.
        self.lineage = CanonicalLineage((self.v3, self.v1, self.v2))

    def test_subject_identity_is_stable_across_immutable_versions(self) -> None:
        self.assertEqual(
            {record.subject_id for record in self.lineage.records},
            {self.v1.subject_id},
        )
        self.assertEqual(len({record.version_id for record in self.lineage.records}), 3)

    def test_head_is_latest_admitted_version_by_predecessor_lineage(self) -> None:
        self.assertIs(self.lineage.head, self.v3)

    def test_future_effective_head_can_differ_from_effective_version(self) -> None:
        effective = self.lineage.resolve_effective(
            at=at("2026-08-15T12:00:00+00:00")
        )

        self.assertIs(self.lineage.head, self.v3)
        self.assertIs(effective, self.v1)
        self.assertNotEqual(self.lineage.head.version_id, effective.version_id)

    def test_effective_version_changes_at_half_open_boundary(self) -> None:
        before = self.lineage.resolve_effective(
            at=at("2026-08-31T23:59:59+00:00")
        )
        at_boundary = self.lineage.resolve_effective(
            at=at("2026-09-01T00:00:00+00:00")
        )

        self.assertIs(before, self.v1)
        self.assertIs(at_boundary, self.v2)

    def test_historical_effective_resolution_does_not_follow_current_head(self) -> None:
        self.assertIs(
            self.lineage.resolve_effective(at=at("2026-09-15T00:00:00+00:00")),
            self.v2,
        )
        self.assertIs(self.lineage.head, self.v3)

    def test_exact_version_identity_remains_resolvable_for_consequential_pinning(self) -> None:
        resolved = self.lineage.resolve_version(self.v1.version_id)
        pin = GovernedVersionPin.from_record(resolved)

        self.assertIs(resolved, self.v1)
        self.assertEqual(pin.subject_id, self.v1.subject_id)
        self.assertEqual(pin.version_id, self.v1.version_id)
        self.assertNotEqual(pin.version_id, self.lineage.head.version_id)

    def test_unknown_exact_version_fails_explicitly(self) -> None:
        with self.assertRaises(CanonicalVersionNotFoundError):
            self.lineage.resolve_version(
                Identity(
                    "canonical-version",
                    "subject-1-v404",
                    self.v1.organization.organization_id.value,
                )
            )

    def test_competing_admitted_successors_are_rejected_as_ambiguous_head(self) -> None:
        competing = replace(
            self.v2,
            version_id=Identity(
                "canonical-version",
                "subject-1-v2-competing",
                self.v1.organization.organization_id.value,
            ),
            payload=(("label", "competing successor"),),
        )

        with self.assertRaises(CanonicalLineageConflictError):
            CanonicalLineage((self.v1, self.v2, competing))

    def test_missing_predecessor_is_rejected_instead_of_guessed(self) -> None:
        orphan = replace(
            self.v2,
            predecessor_version_id=Identity(
                "canonical-version",
                "missing-predecessor",
                self.v1.organization.organization_id.value,
            ),
        )

        with self.assertRaises(CanonicalLineageConflictError):
            CanonicalLineage((self.v1, orphan))

    def test_mixed_subjects_cannot_be_collapsed_into_one_lineage(self) -> None:
        other_subject = replace(
            self.v2,
            subject_id=Identity(
                "canonical-subject",
                "subject-2",
                self.v1.organization.organization_id.value,
            ),
        )

        with self.assertRaises(CanonicalLineageConflictError):
            CanonicalLineage((self.v1, other_subject))

    def test_mixed_authority_scope_cannot_be_collapsed_into_one_lineage(self) -> None:
        other_scope = replace(self.v2, authority_scope="reference.subject/other-state")

        with self.assertRaises(CanonicalLineageConflictError):
            CanonicalLineage((self.v1, other_scope))

    def test_overlapping_effective_periods_fail_explicitly(self) -> None:
        overlapping_v1 = replace(
            self.v1,
            effective_until=at("2026-09-10T00:00:00+00:00"),
        )
        overlapping_lineage = CanonicalLineage((overlapping_v1, self.v2, self.v3))

        with self.assertRaises(AmbiguousEffectiveVersionError):
            overlapping_lineage.resolve_effective(
                at=at("2026-09-05T00:00:00+00:00")
            )

    def test_gap_in_effective_periods_fails_explicitly(self) -> None:
        delayed_v2 = replace(
            self.v2,
            effective_from=at("2026-09-10T00:00:00+00:00"),
        )
        gap_lineage = CanonicalLineage((self.v1, delayed_v2, self.v3))

        with self.assertRaises(NoEffectiveVersionError):
            gap_lineage.resolve_effective(at=at("2026-09-05T00:00:00+00:00"))

    def test_effective_resolution_requires_timezone_aware_context(self) -> None:
        with self.assertRaises(ValueError):
            self.lineage.resolve_effective(at=datetime(2026, 8, 15, 12, 0, 0))


class P202SecondLineageIntegrationTests(unittest.TestCase):
    def test_second_subject_immediate_effect_lineage_resolves_independently(self) -> None:
        scenario = build_p1_reference_scenario()
        base = scenario.input_record
        subject = Identity(
            "canonical-subject",
            "subject-2",
            base.organization.organization_id.value,
        )
        switch = at("2026-08-20T00:00:00+00:00")
        first: CanonicalRecord = replace(
            base,
            subject_id=subject,
            version_id=Identity(
                "canonical-version",
                "subject-2-v1",
                base.organization.organization_id.value,
            ),
            effective_from=at("2026-08-01T00:00:00+00:00"),
            effective_until=switch,
        )
        second = replace(
            first,
            version_id=Identity(
                "canonical-version",
                "subject-2-v2",
                base.organization.organization_id.value,
            ),
            created_at=at("2026-08-20T00:00:00+00:00"),
            predecessor_version_id=first.version_id,
            effective_from=switch,
            effective_until=None,
        )
        lineage = CanonicalLineage((second, first))

        self.assertEqual(lineage.subject_id, subject)
        self.assertIs(lineage.head, second)
        self.assertIs(
            lineage.resolve_effective(at=at("2026-08-20T00:00:00+00:00")),
            second,
        )
        self.assertEqual(
            GovernedVersionPin.from_record(lineage.resolve_effective(at=switch)).version_id,
            second.version_id,
        )


if __name__ == "__main__":
    unittest.main()
