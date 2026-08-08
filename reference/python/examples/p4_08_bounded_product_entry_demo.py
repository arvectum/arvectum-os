from __future__ import annotations

from datetime import datetime, timezone
from html import escape

from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_002_MEMORY_KNOWLEDGE,
    CAPABILITY_CONTRACT_VERSION,
    OP_RESOLVE_DOCUMENT,
    OP_RETRIEVE_KNOWLEDGE,
    CapabilityConsumptionRequest,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import render_workspace_shell_html
from bounded_product_ref.contract import (
    PRODUCT_VERSION,
    build_p4_08_product_contract,
    product_id_for,
)
from bounded_product_ref.task_composition import BoundedProductTask, enter_product_task_workspace


UTC = timezone.utc


def build_demo_html() -> str:
    organization = OrganizationScope(Identity("organization", "org-a", "platform"))
    actor = ActorContext(
        Principal(Identity("principal", "operator-1", "platform")),
        organization,
    )
    product_id = product_id_for(actor)
    contract = build_p4_08_product_contract(
        actor=actor,
        created_at=datetime(2026, 8, 8, 20, 0, tzinfo=UTC),
    )
    task = BoundedProductTask(
        organization=organization,
        product_id=product_id,
        product_version=PRODUCT_VERSION,
        task_id=Identity("product-task", "task-1", "org-a"),
        document_subject_id=Identity("document", "doc-1", "org-a"),
        title="Review governed task context",
    )
    access = AccessRequest(
        actor=actor,
        purpose="bounded-product-review",
        required_right="read",
        allowed_classifications=("internal",),
    )
    requests = (
        CapabilityConsumptionRequest(
            organization=organization,
            product_id=product_id,
            product_version=PRODUCT_VERSION,
            dependency_id=CAP_001_DOCUMENT_ARTIFACT,
            dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
            operation_name=OP_RESOLVE_DOCUMENT,
            access=access,
        ),
        CapabilityConsumptionRequest(
            organization=organization,
            product_id=product_id,
            product_version=PRODUCT_VERSION,
            dependency_id=CAP_002_MEMORY_KNOWLEDGE,
            dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
            operation_name=OP_RETRIEVE_KNOWLEDGE,
            access=access,
        ),
    )
    entry = enter_product_task_workspace(
        contract=contract,
        task=task,
        actor=actor,
        capability_requests=requests,
    )
    shell = render_workspace_shell_html(entry.workspace)
    dependencies = ", ".join(
        escape(admission.dependency_id.value) for admission in entry.capability_admissions
    )
    product_panel = (
        '<section data-product-boundary="bounded-p4.08">'
        '<h2>Bounded product task</h2>'
        f'<p>Task: {escape(task.title)}</p>'
        f'<p>Product-owned task: {escape(task.task_id.value)}</p>'
        f'<p>Declared shared capability entries: {dependencies}</p>'
        '<p>Product Contract entry is context only. Source access and consequential '
        'authority remain independently enforced.</p>'
        '<p>Consequential operator actions are composed through the R10 operator-safety guard.</p>'
        '</section>'
    )
    return '<!doctype html><html><body>' + shell + product_panel + '</body></html>'


if __name__ == "__main__":
    print(build_demo_html())
