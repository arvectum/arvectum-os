from datetime import datetime, timezone
from pathlib import Path
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.canonical_lineage import (
    CanonicalLineage,
    CanonicalLineageConflictError,
    CanonicalVersionNotFoundError,
)
from arvectum_os_ref.event_provenance import EventRuntimeError
from arvectum_os_ref.governed_execution import GovernedExecutionRuntimeError
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.relationships import RelationshipRuntimeError
from arvectum_os_ref.runtime_consistency import (
    RuntimeConsistencyError,
    RuntimeConsistencyState,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal


UTC = timezone.utc
PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "arvectum_os_ref"


class R2RuntimeHealthTests(unittest.TestCase):
    """Cross-cutting R2 fitness evidence over the accumulated Core Runtime spine."""

    def setUp(self) -> None:
        self.organization = OrganizationScope(
            Identity("organization", "org-r2", "platform")
        )
        self.principal = Principal(Identity("principal", "r2-actor", "platform"))
        self.actor = ActorContext(self.principal, self.organization)

    def _id(self, namespace: str, value: str) -> Identity:
        return Identity(namespace, value, "org-r2")

    def _record(
        self,
        *,
        version: str,
        predecessor: Identity | None,
    ) -> CanonicalRecord:
        return CanonicalRecord(
            subject_id=self._id("canonical-subject", "r2-subject"),
            version_id=self._id("canonical-version", version),
            semantic_type="example.r2-subject",
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="example.r2-subject/state",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=datetime(2026, 8, 8, 10, 0, tzinfo=UTC),
            provenance_refs=(self.principal.principal_id,),
            integrity_metadata=(("representation", "r2-test"),),
            payload=(("version", version),),
            lifecycle_status="Active",
            predecessor_version_id=predecessor,
        )

    def _source(self, module_name: str) -> str:
        return (PACKAGE_ROOT / module_name).read_text(encoding="utf-8")

    def test_consistency_reuses_existing_semantic_owners(self) -> None:
        source = self._source("runtime_consistency.py")
        self.assertIn("from .canonical_lineage import CanonicalLineage", source)
        self.assertIn("from .event_provenance import CanonicalEvent, EventReceipt, admit_event", source)
        self.assertIn("require_consequential_operation_admission", source)
        self.assertNotIn("class CanonicalLineage", source)
        self.assertNotIn("def admit_event", source)

    def test_relationship_runtime_reuses_canonical_lineage(self) -> None:
        source = self._source("relationships.py")
        self.assertIn("from .canonical_lineage import CanonicalLineage", source)
        self.assertNotIn("class CanonicalLineage", source)

    def test_accumulated_runtime_does_not_select_durable_infrastructure(self) -> None:
        modules = (
            "canonical_lineage.py",
            "relationships.py",
            "governed_execution.py",
            "event_provenance.py",
            "runtime_consistency.py",
        )
        forbidden_import_markers = (
            "import sqlalchemy",
            "from sqlalchemy",
            "import psycopg",
            "from psycopg",
            "import sqlite3",
            "import kafka",
            "from kafka",
            "import celery",
            "from celery",
        )
        combined = "\n".join(self._source(name).lower() for name in modules)
        for marker in forbidden_import_markers:
            self.assertNotIn(marker, combined)

    def test_runtime_error_families_remain_semantically_scoped(self) -> None:
        self.assertTrue(issubclass(RelationshipRuntimeError, ValueError))
        self.assertTrue(issubclass(GovernedExecutionRuntimeError, RuntimeError))
        self.assertTrue(issubclass(EventRuntimeError, RuntimeError))
        self.assertTrue(issubclass(RuntimeConsistencyError, RuntimeError))
        self.assertTrue(issubclass(CanonicalVersionNotFoundError, ValueError))

    def test_runtime_consistency_state_reuses_fail_closed_lineage_validation(self) -> None:
        root = self._record(version="v1", predecessor=None)
        branch_a = self._record(version="v2-a", predecessor=root.version_id)
        branch_b = self._record(version="v2-b", predecessor=root.version_id)
        with self.assertRaises(CanonicalLineageConflictError):
            RuntimeConsistencyState(canonical_records=(root, branch_a, branch_b))

    def test_exact_version_resolution_remains_distinct_from_head_resolution(self) -> None:
        root = self._record(version="v1", predecessor=None)
        successor = self._record(version="v2", predecessor=root.version_id)
        lineage = CanonicalLineage((successor, root))
        self.assertEqual(lineage.head.version_id, successor.version_id)
        self.assertEqual(lineage.resolve_version(root.version_id), root)
        with self.assertRaises(CanonicalVersionNotFoundError):
            lineage.resolve_version(self._id("canonical-version", "missing"))


if __name__ == "__main__":
    unittest.main()
