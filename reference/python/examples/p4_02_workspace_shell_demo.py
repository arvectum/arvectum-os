"""Render the bounded P4.02 workspace shell as a standalone local HTML demo.

Usage from ``reference/python``::

    python examples/p4_02_workspace_shell_demo.py > /tmp/arvectum-p4-02.html

Open the resulting file in a browser. The document is static demonstration
output only: it establishes no HTTP server, URL/deep-link contract, frontend
framework, IAM/session mechanism, API/BFF boundary or authorization decision.
"""

from __future__ import annotations

from html import escape

from arvectum_os_ref.identity import Identity
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import (
    ExactVersionNavigationReference,
    WorkspaceDestination,
    WorkspaceShellState,
    navigate_workspace,
    open_workspace_shell,
    render_workspace_shell_html,
)


def build_demo() -> str:
    organization = OrganizationScope(
        Identity("organization", "demo-organization", "platform")
    )
    principal = Principal(Identity("principal", "demo-operator", "platform"))
    actor = ActorContext(principal, organization)

    state = open_workspace_shell(actor)
    if not isinstance(state, WorkspaceShellState):
        raise RuntimeError("demo shell unexpectedly failed to resolve Organization context")

    state = navigate_workspace(
        state,
        destination=WorkspaceDestination.RECORDS,
        reference=ExactVersionNavigationReference(
            organization=organization,
            subject_id=Identity("subject", "example-subject", "demo-organization"),
            version_id=Identity("version", "example-version-2", "demo-organization"),
        ),
    )

    shell = render_workspace_shell_html(state)
    title = escape("Arvectum OS — P4.02 workspace shell demo")
    return (
        "<!doctype html>"
        '<html lang="en">'
        "<head>"
        '<meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>{title}</title>"
        "</head>"
        f"<body>{shell}</body>"
        "</html>"
    )


if __name__ == "__main__":
    print(build_demo())
