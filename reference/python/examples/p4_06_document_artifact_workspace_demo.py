"""Render the bounded P4.06 Document / Artifact workspace as static HTML.

Run from ``reference/python``:

    PYTHONPATH=. python examples/p4_06_document_artifact_workspace_demo.py > /tmp/arvectum-p4-06.html

The output is inert presentation evidence. It is not a web application, route
contract, content-delivery API, DMS, storage decision or production interface.
"""

from __future__ import annotations

from datetime import datetime, timezone

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.canonical_inspection import CurrentSourceAuthorization
from arvectum_os_ref.canonical_lineage import CanonicalLineage
from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.document_artifact_experience import (
    DocumentWorkspaceSourceSet,
    inspect_document_workspace,
    render_document_workspace_html,
)
from arvectum_os_ref.document_artifact_governance import (
    DOCUMENT_SEMANTIC_TYPE,
    ArtifactContent,
    DocumentVersionCandidate,
    HandlingConstraints,
    admit_document_version,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import (
    ExactVersionNavigationReference,
    WorkspaceDestination,
    navigate_workspace,
    open_workspace_shell,
    render_workspace_shell_html,
)


def main() -> None:
    organization = OrganizationScope(Identity("organization", "arvectum-demo", "platform"))
    principal = Principal(Identity("principal", "operator-demo", "platform"))
    actor = ActorContext(principal, organization)
    handling = HandlingConstraints(
        classification="Internal",
        purpose="Governed document review",
        rights=("Internal use", "Review"),
        retention_rule="Demo retention rule",
    )
    access_request = AccessRequest(
        actor=actor,
        purpose="Governed document review",
        required_right="Review",
        allowed_classifications=("Internal",),
    )

    document_id = Identity("document", "operating-standard", "arvectum-demo")
    v1 = CanonicalRecord(
        subject_id=document_id,
        version_id=Identity("document-version", "operating-standard-v1", "arvectum-demo"),
        semantic_type=DOCUMENT_SEMANTIC_TYPE,
        schema_version="1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="document/governed-state",
        accountable_owner_id=principal.principal_id,
        creation_actor=actor,
        created_at=datetime(2026, 8, 8, 17, 0, tzinfo=timezone.utc),
        provenance_refs=(principal.principal_id,),
        integrity_metadata=(("representation", "static-demo"),),
        payload=(("title", "Operating standard"),),
        lifecycle_status="admitted",
    )
    v2 = CanonicalRecord(
        subject_id=document_id,
        version_id=Identity("document-version", "operating-standard-v2", "arvectum-demo"),
        semantic_type=DOCUMENT_SEMANTIC_TYPE,
        schema_version="1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="document/governed-state",
        accountable_owner_id=principal.principal_id,
        creation_actor=actor,
        created_at=datetime(2026, 8, 8, 18, 0, tzinfo=timezone.utc),
        provenance_refs=(principal.principal_id,),
        integrity_metadata=(("representation", "static-demo"),),
        payload=(("title", "Operating standard, current head"),),
        lifecycle_status="admitted",
        predecessor_version_id=v1.version_id,
    )

    source_v1 = ArtifactContent(
        artifact_id=Identity("artifact", "standard-v1-source", "arvectum-demo"),
        organization=organization,
        content_ref="content:standard-v1-source",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        integrity_ref="sha256:source-v1-demo",
        rendition_role="authoring",
        handling=handling,
        storage_locator="internal-demo://authoring/source-v1",
    )
    pdf_v1 = source_v1.derive(
        artifact_id=Identity("artifact", "standard-v1-pdf", "arvectum-demo"),
        content_ref="content:standard-v1-pdf",
        media_type="application/pdf",
        integrity_ref="sha256:pdf-v1-demo",
        rendition_role="exchange",
        transformation="render-to-pdf",
        storage_locator="internal-demo://exchange/pdf-v1",
    )
    admitted_v1 = admit_document_version(
        DocumentVersionCandidate(v1, (source_v1, pdf_v1), "exchange")
    )

    source_v2 = ArtifactContent(
        artifact_id=Identity("artifact", "standard-v2-source", "arvectum-demo"),
        organization=organization,
        content_ref="content:standard-v2-source",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        integrity_ref="sha256:source-v2-demo",
        rendition_role="authoring",
        handling=handling,
        storage_locator="internal-demo://authoring/source-v2",
    )
    pdf_v2 = source_v2.derive(
        artifact_id=Identity("artifact", "standard-v2-pdf", "arvectum-demo"),
        content_ref="content:standard-v2-pdf",
        media_type="application/pdf",
        integrity_ref="sha256:pdf-v2-demo",
        rendition_role="exchange",
        transformation="render-to-pdf",
        storage_locator="internal-demo://exchange/pdf-v2",
    )
    admitted_v2 = admit_document_version(
        DocumentVersionCandidate(v2, (source_v2, pdf_v2), "exchange")
    )

    draft_record = CanonicalRecord(
        subject_id=document_id,
        version_id=Identity("document-version", "working-candidate-v3", "arvectum-demo"),
        semantic_type=DOCUMENT_SEMANTIC_TYPE,
        schema_version="1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="document/governed-state",
        accountable_owner_id=principal.principal_id,
        creation_actor=actor,
        created_at=datetime(2026, 8, 8, 19, 0, tzinfo=timezone.utc),
        provenance_refs=(principal.principal_id,),
        integrity_metadata=(("representation", "working-candidate-demo"),),
        payload=(("title", "Generated working candidate"),),
        lifecycle_status="working-candidate",
        predecessor_version_id=v2.version_id,
    )
    generated_draft = ArtifactContent(
        artifact_id=Identity("artifact", "working-candidate-v3-pdf", "arvectum-demo"),
        organization=organization,
        content_ref="content:working-candidate-v3",
        media_type="application/pdf",
        integrity_ref="sha256:working-v3-demo",
        rendition_role="exchange",
        handling=handling,
        storage_locator="internal-demo://working/v3",
    )
    working_candidate = DocumentVersionCandidate(
        draft_record,
        (generated_draft,),
        "exchange",
    )

    opened = open_workspace_shell(
        actor,
        initial_destination=WorkspaceDestination.DOCUMENTS,
    )
    if not hasattr(opened, "organization"):
        raise RuntimeError("demo workspace failed to open")
    workspace = navigate_workspace(
        opened,
        destination=WorkspaceDestination.DOCUMENTS,
        reference=ExactVersionNavigationReference(
            organization=organization,
            subject_id=document_id,
            version_id=v1.version_id,
        ),
    )
    authorization = CurrentSourceAuthorization(
        organization=organization,
        actor_actual_principal_id=principal.principal_id,
        resource_subject_id=document_id,
        decision_version_id=Identity("authorization-version", "document-read-v1", "arvectum-demo"),
        allowed=True,
    )
    inspection = inspect_document_workspace(
        workspace=workspace,
        sources=DocumentWorkspaceSourceSet(
            lineages=(CanonicalLineage((v1, v2)),),
            admitted_versions=(admitted_v1, admitted_v2),
            working_candidates=(working_candidate,),
        ),
        source_authorizations=(authorization,),
        access_request=access_request,
    )

    shell_html = render_workspace_shell_html(workspace)
    document_html = render_document_workspace_html(inspection)
    print(
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        "<title>Arvectum OS P4.06 Document / Artifact workspace</title>"
        "<style>body{font-family:system-ui,sans-serif;max-width:1200px;margin:2rem auto;padding:0 1rem;line-height:1.45}"
        "header div,nav{display:flex;gap:1rem;flex-wrap:wrap;margin:.75rem 0}button{padding:.45rem .7rem}"
        "section{margin-top:2rem;border-top:1px solid #bbb;padding-top:1.25rem}dl{display:grid;grid-template-columns:14rem 1fr;gap:.35rem 1rem}"
        "dt{font-weight:700}table{border-collapse:collapse;width:100%;font-size:.88rem}th,td{border:1px solid #bbb;padding:.45rem;text-align:left;vertical-align:top}"
        "article{border:1px solid #bbb;padding:1rem;margin:.75rem 0}</style></head><body>"
        f"{shell_html}{document_html}</body></html>"
    )


if __name__ == "__main__":
    main()
