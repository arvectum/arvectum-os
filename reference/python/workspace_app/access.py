from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from arvectum_os_ref.identity import Identity
import p7_04_persistent_access as p704


WORKSPACE_OPERATION = "workspace.open"
WORKSPACE_RESOURCE = "productive-workspace"


class WorkspaceAccessError(RuntimeError):
    pass


@dataclass(frozen=True)
class AccessContext:
    organization: Identity
    actor: Identity
    principal_kind: str
    credential_id: str
    grant_id: str
    authentication_source: str = "P7.04 owner-local credential"


class AccessResolver(Protocol):
    def authorize(self) -> AccessContext:
        ...


def _identity(value: dict[str, str]) -> Identity:
    return Identity(value["namespace"], value["value"], value["scope"])


class P704AccessResolver:
    """Resolve the activated owner-operated Workspace identity server-side."""

    def __init__(self, runtime_root: Path):
        self.runtime_root = runtime_root.expanduser()

    def _selected(self) -> tuple[Identity, Identity, str, Path]:
        state = p704.load_access_store(self.runtime_root)
        organization = _identity(state["organization"])
        humans = [
            (key, record)
            for key, record in state["principals"].items()
            if record["kind"] == "human" and record["status"] == "enabled"
        ]
        if len(humans) != 1:
            raise WorkspaceAccessError("Workspace requires exactly one enabled human principal in the activated owner-operated scope")
        principal_key, human = humans[0]
        actor = _identity(human["identity"])
        active_credentials = [
            record
            for record in state["credentials"].values()
            if record["principal_key"] == principal_key and record["status"] == "active"
        ]
        if len(active_credentials) != 1:
            raise WorkspaceAccessError("Workspace requires exactly one active credential for the selected human principal")
        credential_id = active_credentials[0]["credential_id"]
        credential_file = self.runtime_root / "secrets" / "p7-04" / f"{credential_id}.secret"
        return organization, actor, credential_id, credential_file

    def authorize(self) -> AccessContext:
        organization, actor, credential_id, credential_file = self._selected()
        decision = p704.authorize_from_credential_file(
            self.runtime_root,
            organization=organization,
            principal=actor,
            credential_id=credential_id,
            credential_file=credential_file,
            operation=WORKSPACE_OPERATION,
            resource=WORKSPACE_RESOURCE,
            access_path="local",
        )
        if not decision.allowed:
            raise WorkspaceAccessError(f"Workspace operational access denied: {decision.reason}")
        if decision.principal_kind != "human" or not decision.grant_id:
            raise WorkspaceAccessError("Workspace access decision lacks an attributable human/grant binding")
        return AccessContext(
            organization=organization,
            actor=actor,
            principal_kind=decision.principal_kind,
            credential_id=credential_id,
            grant_id=decision.grant_id,
        )


def provision_workspace_grant(runtime_root: Path) -> str:
    """Provision only the exact local P9.03 shell-open operational grant."""

    resolver = P704AccessResolver(runtime_root)
    state = p704.load_access_store(runtime_root.expanduser())
    organization = _identity(state["organization"])
    humans = [
        (key, record)
        for key, record in state["principals"].items()
        if record["kind"] == "human" and record["status"] == "enabled"
    ]
    if len(humans) != 1:
        raise WorkspaceAccessError("cannot provision Workspace grant with ambiguous enabled human principals")
    principal_key, human = humans[0]
    actor = _identity(human["identity"])
    for record in state["grants"].values():
        if (
            record["principal_key"] == principal_key
            and record["organization"] == {"namespace": organization.namespace, "value": organization.value, "scope": organization.scope}
            and record["operation"] == WORKSPACE_OPERATION
            and record["resource"] == WORKSPACE_RESOURCE
            and record["status"] == "active"
            and "local" in record["access_paths"]
        ):
            return record["grant_id"]
    grant_id = p704.grant_access(
        runtime_root.expanduser(),
        actor,
        operation=WORKSPACE_OPERATION,
        resource=WORKSPACE_RESOURCE,
        access_paths=("local",),
    )
    resolver.authorize()
    return grant_id


__all__ = [
    "AccessContext",
    "AccessResolver",
    "P704AccessResolver",
    "WorkspaceAccessError",
    "WORKSPACE_OPERATION",
    "WORKSPACE_RESOURCE",
    "provision_workspace_grant",
]
