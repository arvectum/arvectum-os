from dataclasses import FrozenInstanceError
from datetime import datetime
import inspect
import unittest

from arvectum_os_ref.canonical_lineage import NoEffectiveVersionError
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.reference_scenario import build_p1_reference_scenario
from arvectum_os_ref.relationships import (
    EndpointReferenceRole,
    RelationshipEndpoint,
    RelationshipIdentityChangeRequiredError,
    RelationshipLineageConflictError,
    RelationshipTypeReference,
    RelationshipVersionNotFoundError,
    TraversalDirection,
    TypedRelationshipLineage,
    create_typed_relationship,
    traverse_relationships,
    version_typed_relationship,
)
import arvectum_os_ref.relationships as relationships_module


def at(value: str) -> datetime:
    return datetime.fromisoformat(value)


class P203TypedRelationshipTests(unittest.TestCase):
    def setUp(self) -> None:
        scenario = build_p1_reference_scenario()
        self.organization = scenario.organization
        self.actor = scenario.actor
        self.scope = self.organization.organization_id.value
        self.source = RelationshipEndpoint(
            EndpointReferenceRole.SUBJECT_IDENTITY,
            scenario.input_record.subject_id,
        )
        self.target = RelationshipEndpoint(
            EndpointReferenceRole.SUBJECT_IDENTITY,
            scenario.workflow.record.subject_id,
        )
        self.type_v1 = RelationshipTypeReference(
            type_id=Identity("relationship-type", "related-to", "platform"),
            version_id=Identity(
                "relationship-type-version", "related-to-v1", "platform"
            ),
            semantic_name="related_to",
            schema_version="1",
        )
        self.type_v2 = RelationshipTypeReference(
            type_id=self.type_v1.type_id,
            version_id=Identity(
                "relationship-type-version", "related-to-v2", "platform"
            ),
            semantic_name="related_to",
            schema_version="2",
        )
        self.relationship = self._create("relationship-1", "relationship-1-v1")

    def _create(
        self,
        relationship_name: str,
        version_name: str,
        *,
        relationship_type: RelationshipTypeReference | None = None,
        source: RelationshipEndpoint | None = None,
        target: RelationshipEndpoint | None = None,
        lifecycle_status: str | None = "Active",
        effective_from: datetime | None = None,
        effective_until: datetime | None = None,
    ):
        return create_typed_relationship(
            relationship_id=Identity("relationship", relationship_name, self.scope),
            version_id=Identity("relationship-version", version_name, self.scope),
            relationship_type=relationship_type or self.type_v1,
            source=source or self.source,
            target=target or self.target,
            organization=self.organization,
            actor=self.actor,
            authority_scope="platform.relationship/assertion",
            created_at=at("2026-08-08T07:30:00+00:00"),
            lifecycle_status=lifecycle_status,
            effective_from=effective_from,
            effective_until=effective_until,
        )

    def test_relationship_identity_and_version_identity_are_independent(self) -> None:
        relationship = self.relationship

        self.assertNotEqual(
            relationship.relationship_id,
            relationship.relationship_version_id,
        )
        self.assertEqual(relationship.record.subject_id, relationship.relationship_id)
        self.assertEqual(
            relationship.record.version_id,
            relationship.relationship_version_id,
        )
        self.assertEqual(
            relationship.record.semantic_type,
            "platform.typed-relationship",
        )

    def test_identity_is_not_derived_from_source_type_target_tuple(self) -> None:
        other = self._create("relationship-2", "relationship-2-v1")

        self.assertEqual(other.relationship_type, self.relationship.relationship_type)
        self.assertEqual(other.source, self.relationship.source)
        self.assertEqual(other.target, self.relationship.target)
        self.assertNotEqual(other.relationship_id, self.relationship.relationship_id)

    def test_relationship_preserves_type_schema_and_exact_type_version(self) -> None:
        relationship = self.relationship

        self.assertEqual(relationship.relationship_type.semantic_name, "related_to")
        self.assertEqual(relationship.relationship_type.schema_version, "1")
        self.assertIn(
            relationship.relationship_type.type_id,
            relationship.record.provenance_refs,
        )
        self.assertIn(
            relationship.relationship_type.version_id,
            relationship.record.provenance_refs,
        )

    def test_subject_and_version_endpoint_roles_are_explicit_and_distinct(self) -> None:
        underlying = self.source.identity
        subject_ref = RelationshipEndpoint(
            EndpointReferenceRole.SUBJECT_IDENTITY,
            underlying,
        )
        version_ref = RelationshipEndpoint(
            EndpointReferenceRole.VERSION_IDENTITY,
            underlying,
        )

        self.assertNotEqual(subject_ref, version_ref)
        self.assertEqual(subject_ref.identity, version_ref.identity)

    def test_version_pinned_endpoint_is_preserved_exactly(self) -> None:
        scenario = build_p1_reference_scenario()
        version_source = RelationshipEndpoint(
            EndpointReferenceRole.VERSION_IDENTITY,
            scenario.input_record.version_id,
        )
        relationship = self._create(
            "relationship-version-pinned",
            "relationship-version-pinned-v1",
            source=version_source,
        )

        self.assertIs(
            relationship.source.reference_role,
            EndpointReferenceRole.VERSION_IDENTITY,
        )
        self.assertEqual(relationship.source.identity, scenario.input_record.version_id)

    def test_bounded_runtime_rejects_cross_organization_endpoint(self) -> None:
        other_scope_target = RelationshipEndpoint(
            EndpointReferenceRole.SUBJECT_IDENTITY,
            Identity("canonical-subject", "external-subject", "org-b"),
        )

        with self.assertRaises(ValueError):
            self._create(
                "relationship-cross-org",
                "relationship-cross-org-v1",
                target=other_scope_target,
            )

    def test_relationship_version_is_immutable(self) -> None:
        with self.assertRaises(FrozenInstanceError):
            self.relationship.source = self.target  # type: ignore[misc]

    def test_backward_compatible_type_definition_update_can_version_same_assertion(self) -> None:
        successor = version_typed_relationship(
            self.relationship,
            version_id=Identity(
                "relationship-version", "relationship-1-v2", self.scope
            ),
            actor=self.actor,
            created_at=at("2026-08-08T08:00:00+00:00"),
            relationship_type=self.type_v2,
        )

        self.assertEqual(successor.relationship_id, self.relationship.relationship_id)
        self.assertEqual(
            successor.record.predecessor_version_id,
            self.relationship.relationship_version_id,
        )
        self.assertEqual(successor.relationship_type.version_id, self.type_v2.version_id)
        self.assertEqual(self.relationship.relationship_type.version_id, self.type_v1.version_id)

    def test_semantic_relationship_type_change_requires_new_identity(self) -> None:
        changed_type = RelationshipTypeReference(
            type_id=self.type_v1.type_id,
            version_id=Identity(
                "relationship-type-version", "related-to-v3", "platform"
            ),
            semantic_name="owned_by",
            schema_version="1",
        )

        with self.assertRaises(RelationshipIdentityChangeRequiredError):
            version_typed_relationship(
                self.relationship,
                version_id=Identity(
                    "relationship-version", "relationship-1-v2", self.scope
                ),
                actor=self.actor,
                created_at=at("2026-08-08T08:00:00+00:00"),
                relationship_type=changed_type,
            )

    def test_source_identity_change_requires_new_relationship_identity(self) -> None:
        changed_source = RelationshipEndpoint(
            EndpointReferenceRole.SUBJECT_IDENTITY,
            Identity("canonical-subject", "another-source", self.scope),
        )

        with self.assertRaises(RelationshipIdentityChangeRequiredError):
            version_typed_relationship(
                self.relationship,
                version_id=Identity(
                    "relationship-version", "relationship-1-v2", self.scope
                ),
                actor=self.actor,
                created_at=at("2026-08-08T08:00:00+00:00"),
                source=changed_source,
            )

    def test_source_reference_role_change_requires_new_relationship_identity(self) -> None:
        changed_role = RelationshipEndpoint(
            EndpointReferenceRole.VERSION_IDENTITY,
            self.relationship.source.identity,
        )

        with self.assertRaises(RelationshipIdentityChangeRequiredError):
            version_typed_relationship(
                self.relationship,
                version_id=Identity(
                    "relationship-version", "relationship-1-v2", self.scope
                ),
                actor=self.actor,
                created_at=at("2026-08-08T08:00:00+00:00"),
                source=changed_role,
            )

    def test_target_change_requires_new_relationship_identity(self) -> None:
        changed_target = RelationshipEndpoint(
            EndpointReferenceRole.SUBJECT_IDENTITY,
            Identity("workflow-subject", "another-workflow", self.scope),
        )

        with self.assertRaises(RelationshipIdentityChangeRequiredError):
            version_typed_relationship(
                self.relationship,
                version_id=Identity(
                    "relationship-version", "relationship-1-v2", self.scope
                ),
                actor=self.actor,
                created_at=at("2026-08-08T08:00:00+00:00"),
                target=changed_target,
            )

    def test_lineage_resolves_head_and_exact_historical_version(self) -> None:
        v2 = version_typed_relationship(
            self.relationship,
            version_id=Identity(
                "relationship-version", "relationship-1-v2", self.scope
            ),
            actor=self.actor,
            created_at=at("2026-08-08T08:00:00+00:00"),
            relationship_type=self.type_v2,
        )
        lineage = TypedRelationshipLineage((v2, self.relationship))

        self.assertIs(lineage.head, v2)
        self.assertIs(
            lineage.resolve_version(self.relationship.relationship_version_id),
            self.relationship,
        )

    def test_unknown_exact_relationship_version_fails_explicitly(self) -> None:
        lineage = TypedRelationshipLineage((self.relationship,))

        with self.assertRaises(RelationshipVersionNotFoundError):
            lineage.resolve_version(
                Identity("relationship-version", "missing", self.scope)
            )

    def test_lineage_rejects_assertion_semantic_drift_under_same_identity(self) -> None:
        changed_target = RelationshipEndpoint(
            EndpointReferenceRole.SUBJECT_IDENTITY,
            Identity("workflow-subject", "different-target", self.scope),
        )
        conflicting = create_typed_relationship(
            relationship_id=self.relationship.relationship_id,
            version_id=Identity(
                "relationship-version", "relationship-1-v2-conflict", self.scope
            ),
            relationship_type=self.type_v1,
            source=self.source,
            target=changed_target,
            organization=self.organization,
            actor=self.actor,
            authority_scope="platform.relationship/assertion",
            created_at=at("2026-08-08T08:00:00+00:00"),
        )

        with self.assertRaises(RelationshipLineageConflictError):
            TypedRelationshipLineage((self.relationship, conflicting))

    def test_effective_relationship_resolution_reuses_canonical_half_open_semantics(self) -> None:
        boundary = at("2026-09-01T00:00:00+00:00")
        v1 = self._create(
            "relationship-effective",
            "relationship-effective-v1",
            effective_from=at("2026-08-01T00:00:00+00:00"),
            effective_until=boundary,
        )
        v2 = version_typed_relationship(
            v1,
            version_id=Identity(
                "relationship-version", "relationship-effective-v2", self.scope
            ),
            actor=self.actor,
            created_at=at("2026-08-20T00:00:00+00:00"),
            effective_from=boundary,
            effective_until=None,
        )
        lineage = TypedRelationshipLineage((v2, v1))

        self.assertIs(
            lineage.resolve_effective(at=at("2026-08-15T00:00:00+00:00")),
            v1,
        )
        self.assertIs(lineage.resolve_effective(at=boundary), v2)

    def test_no_effective_relationship_fails_instead_of_guessing(self) -> None:
        relationship = self._create(
            "relationship-future",
            "relationship-future-v1",
            effective_from=at("2026-09-01T00:00:00+00:00"),
        )
        lineage = TypedRelationshipLineage((relationship,))

        with self.assertRaises(NoEffectiveVersionError):
            lineage.resolve_effective(at=at("2026-08-15T00:00:00+00:00"))

    def test_termination_is_new_version_and_prior_active_history_is_preserved(self) -> None:
        terminated = version_typed_relationship(
            self.relationship,
            version_id=Identity(
                "relationship-version", "relationship-1-v2-terminated", self.scope
            ),
            actor=self.actor,
            created_at=at("2026-08-09T00:00:00+00:00"),
            lifecycle_status="Terminated",
        )
        lineage = TypedRelationshipLineage((terminated, self.relationship))

        self.assertEqual(self.relationship.record.lifecycle_status, "Active")
        self.assertEqual(terminated.record.lifecycle_status, "Terminated")
        self.assertIs(lineage.head, terminated)
        self.assertIs(
            lineage.resolve_version(self.relationship.relationship_version_id),
            self.relationship,
        )

    def test_relationship_existence_does_not_intrinsically_grant_authorization_or_authority(self) -> None:
        self.assertFalse(self.relationship.intrinsically_grants_authorization)
        self.assertFalse(
            self.relationship.intrinsically_grants_organizational_authority
        )

    def test_outbound_traversal_preserves_direction_and_exact_endpoint(self) -> None:
        match = traverse_relationships(
            (self.relationship,),
            endpoint=self.source,
            direction=TraversalDirection.OUTBOUND,
        )

        self.assertEqual(len(match), 1)
        self.assertIs(match[0].relationship, self.relationship)
        self.assertEqual(match[0].matched_endpoint, self.source)
        self.assertEqual(match[0].opposite_endpoint, self.target)
        self.assertIs(match[0].direction, TraversalDirection.OUTBOUND)

    def test_inbound_traversal_preserves_direction(self) -> None:
        match = traverse_relationships(
            (self.relationship,),
            endpoint=self.target,
            direction=TraversalDirection.INBOUND,
        )

        self.assertEqual(len(match), 1)
        self.assertEqual(match[0].opposite_endpoint, self.source)
        self.assertIs(match[0].direction, TraversalDirection.INBOUND)

    def test_traversal_does_not_conflate_subject_and_version_endpoint_roles(self) -> None:
        same_identity_wrong_role = RelationshipEndpoint(
            EndpointReferenceRole.VERSION_IDENTITY,
            self.source.identity,
        )

        self.assertEqual(
            traverse_relationships(
                (self.relationship,),
                endpoint=same_identity_wrong_role,
                direction=TraversalDirection.OUTBOUND,
            ),
            (),
        )

    def test_traversal_can_return_distinct_assertion_instances_for_same_tuple(self) -> None:
        other = self._create("relationship-2", "relationship-2-v1")

        matches = traverse_relationships(
            (self.relationship, other),
            endpoint=self.source,
            direction=TraversalDirection.OUTBOUND,
        )

        self.assertEqual(len(matches), 2)
        self.assertEqual(
            {match.relationship.relationship_id for match in matches},
            {self.relationship.relationship_id, other.relationship_id},
        )

    def test_traversal_requires_explicit_direction(self) -> None:
        with self.assertRaises(TypeError):
            traverse_relationships(
                (self.relationship,),
                endpoint=self.source,
                direction="outbound",  # type: ignore[arg-type]
            )

    def test_runtime_has_no_graph_database_dependency(self) -> None:
        source = inspect.getsource(relationships_module).lower()

        self.assertNotIn("neo4j", source)
        self.assertNotIn("networkx", source)
        self.assertNotIn("gremlin", source)


if __name__ == "__main__":
    unittest.main()
