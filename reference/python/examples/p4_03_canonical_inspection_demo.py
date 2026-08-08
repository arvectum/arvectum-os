"""Render the bounded P4.03 Canonical Record / Relationship inspection demo.

Usage from ``reference/python``::

    python examples/p4_03_canonical_inspection_demo.py > /tmp/arvectum-p4-03.html

The document is static demonstration output only. It establishes no HTTP
server, route/deep-link schema, frontend framework, public API/BFF, IAM/session
mechanism, durable read model or authorization policy. The caller-supplied
``CurrentSourceAuthorization`` values stand in only for current decisions from
the owning authorization/data-governance boundary.
"""

from __future__ import annotations

from datetime import datetime, timezone
from html import escape

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.canonical_inspection import (
    CurrentSourceAuthorization,
    GovernedInspectionSourceSet,
    inspect_current_workspace_reference,
    render_canonical_inspection_html,
)
from arvectum_os_ref.canonical_lineage import CanonicalLineage
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.relationships import (
    EndpointReferenceRole,
    RelationshipEndpoint,
    RelationshipTypeReference,
    TypedRelationshipLineage,
    create_typed_relationship,
    version_typed_relationship,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import (
    ExactVersionNavigationReference,
    SubjectNavigationReference,
    WorkspaceDestination,
    WorkspaceShellState,
    navigate_workspace,
    open_workspace_shell,
)


def _record(
    *,
    subject_id: Identity,
    version_id: Identity,
    organization: OrganizationScope,
    actor: ActorContext,
    created_at: datetime,
    predecessor_version_id: Identity | None,
    effective_from: datetime,
    effective_until: datetime | None,
    label: str,
) -> CanonicalRecord:
    return CanonicalRecord(
        subject_id=subject_id,
        version_id=version_id,
        semantic_type="platform.reference-subject",
        schema_version="1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="platform.reference-subject/state",
        accountable_owner_id=actor.actual_principal.principal_id,
        creation_actor=actor,
        created_at=created_at,
        provenance_refs=(actor.actual_principal.principal_id,),
        integrity_metadata=(("representation", "p4.03-static-demo"),),
        payload=(("label", label),),
        lifecycle_status="Established",
        predecessor_version_id=predecessor_version_id,
        effective_from=effective_from,
        effective_until=effective_until,
    )


def build_demo() -> str:
    organization = OrganizationScope(
        Identity("organization", "demo-organization", "platform")
    )
    principal = Principal(Identity("principal", "demo-operator", "platform"))
    actor = ActorContext(principal, organization)
    subject_id = Identity("subject", "demo-standard", "demo-organization")
    v1_id = Identity("canonical-version", "demo-standard-v1", "demo-organization")
    v2_id = Identity("canonical-version", "demo-standard-v2", "demo-organization")

    v1 = _record(
        subject_id=subject_id,
        version_id=v1_id,
        organization=organization,
        actor=actor,
        created_at=datetime(2026, 7, 1, tzinfo=timezone.utc),
        predecessor_version_id=None,
        effective_from=datetime(2026, 7, 1, tzinfo=timezone.utc),
        effective_until=datetime(2026, 9, 1, tzinfo=timezone.utc),
        label="Current effective standard",
    )
    v2 = _record(
        subject_id=subject_id,
        version_id=v2_id,
        organization=organization,
        actor=actor,
        created_at=datetime(2026, 8, 7, tzinfo=timezone.utc),
        predecessor_version_id=v1_id,
        effective_from=datetime(2026, 9, 1, tzinfo=timezone.utc),
        effective_until=None,
        label="Future-effective admitted head",
    )
    record_lineage = CanonicalLineage((v1, v2))

    relationship_id = Identity("relationship", "demo-dependency", "demo-organization")
    relationship_type = RelationshipTypeReference(
        type_id=Identity("relationship-type", "depends-on", "platform"),
        version_id=Identity("relationship-type-version", "depends-on-v1", "platform"),
        semantic_name="platform.depends-on",
        schema_version="1",
    )
    r1 = create_typed_relationship(
        relationship_id=relationship_id,
        version_id=Identity(
            "relationship-version", "demo-dependency-v1", "demo-organization"
        ),
        relationship_type=relationship_type,
        source=RelationshipEndpoint(EndpointReferenceRole.SUBJECT_IDENTITY, subject_id),
        target=RelationshipEndpoint(
            EndpointReferenceRole.SUBJECT_IDENTITY,
            Identity("subject", "demo-policy", "demo-organization"),
        ),
        organization=organization,
        actor=actor,
        authority_scope="platform.relationship/state",
        created_at=datetime(2026, 7, 1, tzinfo=timezone.utc),
        lifecycle_status="Active",
        effective_from=datetime(2026, 7, 1, tzinfo=timezone.utc),
        effective_until=datetime(2026, 9, 1, tzinfo=timezone.utc),
    )
    r2 = version_typed_relationship(
        r1,
        version_id=Identity(
            "relationship-version", "demo-dependency-v2", "demo-organization"
        ),
        actor=actor,
        created_at=datetime(2026, 8, 7, tzinfo=timezone.utc),
        effective_from=datetime(2026, 9, 1, tzinfo=timezone.utc),
        effective_until=None,
    )
    relationship_lineage = TypedRelationshipLineage((r1, r2))
    sources = GovernedInspectionSourceSet((record_lineage,), (relationship_lineage,))

    def allow(subject: Identity, suffix: str) -> CurrentSourceAuthorization:
        return CurrentSourceAuthorization(
            organization=organization,
            actor_actual_principal_id=principal.principal_id,
            resource_subject_id=subject,
            decision_version_id=Identity(
                "authorization-decision-version",
                f"demo-allow-{suffix}",
                "demo-organization",
            ),
            allowed=True,
        )

    authorizations = (
        allow(subject_id, "record"),
        allow(relationship_id, "relationship"),
    )
    effective_at = datetime(2026, 8, 8, 12, tzinfo=timezone.utc)

    state = open_workspace_shell(actor)
    if not isinstance(state, WorkspaceShellState):
        raise RuntimeError("demo shell unexpectedly failed to resolve Organization context")
    record_state = navigate_workspace(
        state,
        destination=WorkspaceDestination.RECORDS,
        reference=ExactVersionNavigationReference(organization, subject_id, v1_id),
    )
    record_view = inspect_current_workspace_reference(
        record_state,
        sources=sources,
        authorizations=authorizations,
        effective_at=effective_at,
    )

    relationship_state = navigate_workspace(
        state,
        destination=WorkspaceDestination.RECORDS,
        reference=SubjectNavigationReference(organization, relationship_id),
    )
    relationship_view = inspect_current_workspace_reference(
        relationship_state,
        sources=sources,
        authorizations=authorizations,
        effective_at=effective_at,
    )

    title = escape("Arvectum OS — P4.03 canonical inspection demo")
    return (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>{title}</title></head><body>"
        '<main><h1>P4.03 bounded inspection experience</h1>'
        '<p>The first panel is an exact historical Canonical Record version; the '
        'second is the Relationship Head. Both independently show Effective Version.</p>'
        + render_canonical_inspection_html(record_view)
        + render_canonical_inspection_html(relationship_view)
        + "</main></body></html>"
    )


if __name__ == "__main__":
    print(build_demo())
