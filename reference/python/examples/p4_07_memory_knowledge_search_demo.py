"""Render the bounded P4.07 Memory / Knowledge / Search discovery as static HTML.

Run from ``reference/python``:

    PYTHONPATH=. python examples/p4_07_memory_knowledge_search_demo.py > /tmp/arvectum-p4-07.html

The output is inert presentation evidence, not a search/RAG product, public API,
frontend contract, durable read model, vector store or Knowledge authority path.
"""

from __future__ import annotations

from datetime import datetime, timezone

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.canonical_inspection import CurrentSourceAuthorization
from arvectum_os_ref.canonical_lineage import CanonicalLineage
from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.memory_knowledge_governance import (
    KNOWLEDGE_SEMANTIC_TYPE,
    MEMORY_SEMANTIC_TYPE,
    KnowledgeCandidate,
    KnowledgeConstraints,
    LearningRole,
    MemoryItem,
    Observation,
    ValidatedKnowledge,
)
from arvectum_os_ref.memory_knowledge_search_experience import (
    MemoryKnowledgeSearchSources,
    ObservationSource,
    discover_search,
    inspect_knowledge_workspace,
    render_knowledge_workspace_html,
    render_search_discovery_html,
)
from arvectum_os_ref.search_index_projection import (
    DiscoveryConstraints,
    GovernedSearchSource,
    rebuild_projection,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import (
    WorkspaceDestination,
    navigate_workspace,
    open_workspace_shell,
    render_workspace_shell_html,
)


def record(
    *,
    organization: OrganizationScope,
    actor: ActorContext,
    subject: str,
    version: str,
    semantic_type: str,
    payload: tuple[tuple[str, str], ...],
) -> CanonicalRecord:
    return CanonicalRecord(
        subject_id=Identity("subject", subject, "arvectum-demo"),
        version_id=Identity("version", version, "arvectum-demo"),
        semantic_type=semantic_type,
        schema_version="1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope=f"{semantic_type}/demo-scope",
        accountable_owner_id=actor.actual_principal.principal_id,
        creation_actor=actor,
        created_at=datetime(2026, 8, 8, 19, 30, tzinfo=timezone.utc),
        provenance_refs=(Identity("evidence", f"e-{version}", "arvectum-demo"),),
        integrity_metadata=(("representation", "static-demo"),),
        payload=payload,
        lifecycle_status="governed",
    )


def authorization(
    organization: OrganizationScope,
    actor: ActorContext,
    resource: Identity,
) -> CurrentSourceAuthorization:
    return CurrentSourceAuthorization(
        organization=organization,
        actor_actual_principal_id=actor.actual_principal.principal_id,
        resource_subject_id=resource,
        decision_version_id=Identity(
            "authorization-version", f"allow-{resource.value}", "arvectum-demo"
        ),
        allowed=True,
    )


def main() -> None:
    organization = OrganizationScope(
        Identity("organization", "arvectum-demo", "platform")
    )
    principal = Principal(Identity("principal", "operator-demo", "platform"))
    actor = ActorContext(principal, organization)
    constraints = KnowledgeConstraints(
        "decision-support", "internal", ("internal-use",), "current"
    )
    request = AccessRequest(
        actor, "decision-support", "internal-use", ("internal",)
    )

    observation = Observation(
        Identity("observation", "delivery-pattern", "arvectum-demo"),
        organization,
        (Identity("event", "delivery-event", "arvectum-demo"),),
        "Repeated delivery delay was observed for one bounded workflow condition.",
    )
    memory_record = record(
        organization=organization,
        actor=actor,
        subject="retained-delivery-context",
        version="retained-delivery-context-v1",
        semantic_type=MEMORY_SEMANTIC_TYPE,
        payload=(("summary", "The organization retained the observed delivery context."),),
    )
    memory = MemoryItem(
        memory_record,
        LearningRole.OBSERVATION,
        memory_record.provenance_refs,
        constraints,
    )
    candidate = KnowledgeCandidate(
        Identity("knowledge-candidate", "delivery-candidate", "arvectum-demo"),
        organization,
        Identity("subject", "delivery-knowledge", "arvectum-demo"),
        "Candidate: the condition may predict a delivery delay.",
        (Identity("evidence", "candidate-evidence", "arvectum-demo"),),
        constraints,
        validation_result="review-in-progress",
    )
    knowledge_record = record(
        organization=organization,
        actor=actor,
        subject="delivery-knowledge",
        version="delivery-knowledge-v1",
        semantic_type=KNOWLEDGE_SEMANTIC_TYPE,
        payload=(("proposition", "Validated: under the declared scope, the condition requires manual review."),),
    )
    knowledge = ValidatedKnowledge(
        knowledge_record,
        knowledge_record.provenance_refs,
        constraints,
        "passed",
        Identity("decision", "approve-delivery-knowledge-v1", "arvectum-demo"),
    )

    discovery_constraints = DiscoveryConstraints(
        "decision-support", "internal", ("internal-use",), "retain-governed"
    )
    search_sources = (
        GovernedSearchSource(
            memory_record,
            "delivery delay retained context",
            discovery_constraints,
        ),
        GovernedSearchSource(
            knowledge_record,
            "delivery delay manual review validated knowledge",
            discovery_constraints,
        ),
    )
    sources = MemoryKnowledgeSearchSources(
        observations=(ObservationSource(observation, constraints),),
        memories=(memory,),
        candidates=(candidate,),
        knowledge=(knowledge,),
        knowledge_lineages=(CanonicalLineage((knowledge_record,)),),
        search_projection=rebuild_projection(sources=search_sources),
        search_sources=search_sources,
    )
    authorizations = (
        authorization(organization, actor, observation.observation_id),
        authorization(organization, actor, memory_record.subject_id),
        authorization(organization, actor, candidate.candidate_id),
        authorization(organization, actor, knowledge.subject_id),
    )

    opened = open_workspace_shell(
        actor, initial_destination=WorkspaceDestination.KNOWLEDGE
    )
    if not hasattr(opened, "organization"):
        raise RuntimeError("demo workspace failed to open")
    knowledge_view = inspect_knowledge_workspace(
        workspace=opened,
        sources=sources,
        source_authorizations=authorizations,
        access_request=request,
    )
    discover_workspace = navigate_workspace(
        opened, destination=WorkspaceDestination.DISCOVER
    )
    search_view = discover_search(
        workspace=discover_workspace,
        sources=sources,
        source_authorizations=authorizations,
        access_request=request,
        query_text="delivery delay",
    )

    print(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>Arvectum OS P4.07 Memory / Knowledge / Search</title>'
        '<style>body{font-family:system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;line-height:1.45}'
        'header div,nav{display:flex;gap:1rem;flex-wrap:wrap;margin:.75rem 0}button{padding:.45rem .7rem}'
        'section{margin-top:2rem;border-top:1px solid #bbb;padding-top:1.25rem}'
        'article{border:1px solid #bbb;padding:1rem;margin:.75rem 0}'
        'dl{display:grid;grid-template-columns:14rem 1fr;gap:.35rem 1rem}dt{font-weight:700}</style>'
        '</head><body>'
        + render_workspace_shell_html(opened)
        + render_knowledge_workspace_html(knowledge_view)
        + render_workspace_shell_html(discover_workspace)
        + render_search_discovery_html(search_view)
        + '</body></html>'
    )


if __name__ == "__main__":
    main()
