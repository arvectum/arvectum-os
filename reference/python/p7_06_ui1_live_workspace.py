#!/usr/bin/env python3
"""P7.06-UI1 — live read-only governed workspace.

Private/reversible owner-operated presentation adapter only.

The adapter:
* runs only from the exact currently activated P7.06 release;
* binds to loopback only;
* authenticates/authorizes every request through the existing P7.04 exact grant;
* resolves the explicit Organization and attributable human Actor before reading
  governed state;
* reads P7.03 immutable governed-item manifests/checkpoints and P7.05 health;
* reuses the Phase-4 workspace shell information architecture;
* renders no payload bytes and exposes no mutation endpoint;
* treats presentation/search/grouping as non-authoritative projections.

It is not a public/stable API, route contract, frontend-framework commitment,
Organizational Authority source, approval mechanism, or canonical state store.
"""

from __future__ import annotations

import argparse
import ipaddress
import os
import sys
from dataclasses import dataclass
from html import escape
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence
from urllib.parse import parse_qs, urlsplit

from arvectum_os_ref.identity import Identity
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import (
    WORKSPACE_DESTINATIONS,
    WorkspaceDestination,
    WorkspaceShellState,
    open_workspace_shell,
)

import p7_03_durable_state as p703
import p7_04_persistent_access as p704
import p7_05_operational_visibility as p705
import p7_06_governed_deploy as p706


WORKSPACE_OPERATION = "workspace.inspect"
WORKSPACE_RESOURCE = "workspace:p7-06-ui1"
WORKSPACE_ACCESS_PATH = "local"
MAX_VISIBLE_ITEMS = 500
MAX_VISIBLE_CHECKPOINTS = 500


class UI1Error(RuntimeError):
    """Base P7.06-UI1 error."""


class UI1AccessDenied(UI1Error):
    """Authentication/authorization failed before governed-state disclosure."""


class UI1IntegrityError(UI1Error):
    """Live runtime/release/state integrity failed closed."""


class UI1BoundaryError(UI1Error):
    """The bounded private/read-only UI1 operating boundary would be crossed."""


@dataclass(frozen=True, slots=True)
class LiveGovernedItem:
    storage_item_id: str
    semantic_type: str
    schema_version: str
    subject_identity: str
    version_identity: str
    authority_mode: str
    authority_scope: str
    authoritative_source: Optional[str]
    classification: str
    lifecycle_status: Optional[str]
    validation_status: Optional[str]
    governed_admission_ref: str
    provenance_refs: tuple[str, ...]
    source_release_sha: str


@dataclass(frozen=True, slots=True)
class LiveCheckpoint:
    checkpoint_id: str
    execution_subject_identity: str
    execution_version_identity: str
    classification: str
    reason: str
    governed_storage_item_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class LiveWorkspaceSnapshot:
    workspace: WorkspaceShellState
    runtime_root: Path
    release_sha: str
    health_state: str
    health_code: str
    health_detail: str
    heartbeat_age_seconds: Optional[float]
    items: tuple[LiveGovernedItem, ...]
    checkpoints: tuple[LiveCheckpoint, ...]
    access_grant_id: str

    @property
    def organization_id(self) -> str:
        return self.workspace.organization.organization_id.value

    @property
    def actor_id(self) -> str:
        return self.workspace.actor.actual_principal.principal_id.value


def _required_text(mapping: Mapping[str, Any], key: str, *, source: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise UI1IntegrityError(f"{source} has no valid {key}")
    return value.strip()


def _optional_text(mapping: Mapping[str, Any], key: str) -> Optional[str]:
    value = mapping.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise UI1IntegrityError(f"governed metadata field {key} has invalid type")
    value = value.strip()
    return value or None


def _identity(raw: Mapping[str, Any], *, label: str) -> Identity:
    if not isinstance(raw, Mapping):
        raise UI1IntegrityError(f"{label} identity is unavailable")
    try:
        return Identity(str(raw["namespace"]), str(raw["value"]), str(raw["scope"]))
    except (KeyError, TypeError, ValueError) as exc:
        raise UI1IntegrityError(f"{label} identity is invalid") from exc


def _verify_loopback_host(host: str) -> str:
    try:
        address = ipaddress.ip_address(host)
    except ValueError as exc:
        raise UI1BoundaryError("UI1 host must be an explicit loopback IP literal") from exc
    if not address.is_loopback:
        raise UI1BoundaryError("UI1 may bind only to loopback in the current private operating boundary")
    if address.version != 4:
        # ThreadingHTTPServer uses AF_INET by default. Keep the initial boundary
        # deterministic instead of silently introducing a second listener family.
        raise UI1BoundaryError("UI1 initial server supports IPv4 loopback only")
    return str(address)


def _verify_exact_release(root: Path) -> str:
    root = root.expanduser().resolve()
    current = p706.current_release(root)
    p706.verify_release(root, current)
    expected = (
        root
        / "releases"
        / current
        / "source"
        / "reference"
        / "python"
        / Path(__file__).name
    )
    if not expected.is_file() or expected.is_symlink():
        raise UI1IntegrityError("UI1 module is missing from the exact current release")
    if Path(__file__).resolve() != expected.resolve():
        raise UI1IntegrityError(
            "UI1 must execute from the exact current release, not a working tree or stale release"
        )
    return current


def _authorize(
    root: Path,
    *,
    organization: Identity,
    principal: Identity,
    credential_id: str,
    credential_file: Path,
) -> p704.AccessDecision:
    decision = p704.authorize_from_credential_file(
        root,
        organization=organization,
        principal=principal,
        credential_id=credential_id,
        credential_file=credential_file,
        operation=WORKSPACE_OPERATION,
        resource=WORKSPACE_RESOURCE,
        access_path=WORKSPACE_ACCESS_PATH,
    )
    if not decision.allowed:
        raise UI1AccessDenied("workspace access is unavailable")
    if decision.principal_kind != "human":
        raise UI1AccessDenied("workspace access is unavailable")
    if decision.organizational_authority_satisfied or decision.consequential_approval_satisfied:
        raise UI1IntegrityError("operational workspace access must not satisfy authority or approval")
    if not isinstance(decision.grant_id, str) or not decision.grant_id:
        raise UI1IntegrityError("allowed workspace access has no attributable exact grant")
    return decision


def _workspace_context(
    organization: Identity,
    principal: Identity,
) -> WorkspaceShellState:
    try:
        organization_scope = OrganizationScope(organization)
        actor = ActorContext(Principal(principal), organization_scope)
    except (TypeError, ValueError) as exc:
        raise UI1AccessDenied("workspace access is unavailable") from exc
    opened = open_workspace_shell(actor)
    if not isinstance(opened, WorkspaceShellState):
        raise UI1AccessDenied("workspace access is unavailable")
    return opened


def _live_items(root: Path) -> tuple[LiveGovernedItem, ...]:
    items_root = root / "state" / "governed" / "items"
    if not items_root.exists():
        raise UI1IntegrityError("governed item root is unavailable")
    if items_root.is_symlink() or not items_root.is_dir():
        raise UI1IntegrityError("governed item root is unsafe")
    entries = sorted(items_root.iterdir(), key=lambda path: path.name)
    if len(entries) > MAX_VISIBLE_ITEMS:
        raise UI1IntegrityError(
            f"live governed item set exceeds UI1 bounded limit ({MAX_VISIBLE_ITEMS})"
        )

    visible: list[LiveGovernedItem] = []
    for item_dir in entries:
        if item_dir.is_symlink() or not item_dir.is_dir():
            raise UI1IntegrityError("unexpected governed item path")
        try:
            manifest = p703.verify_item(item_dir)
        except p703.P703Error as exc:
            raise UI1IntegrityError("governed item integrity verification failed") from exc
        metadata = manifest.get("metadata")
        if not isinstance(metadata, Mapping):
            raise UI1IntegrityError("governed item metadata is unavailable")
        if metadata.get("state_class") != "canonical-governed-state":
            continue
        provenance = metadata.get("provenance_refs")
        if not isinstance(provenance, list) or not all(
            isinstance(value, str) and value.strip() for value in provenance
        ):
            raise UI1IntegrityError("canonical governed item provenance is unavailable")
        visible.append(
            LiveGovernedItem(
                storage_item_id=_required_text(
                    manifest, "storage_item_id", source="governed item manifest"
                ),
                semantic_type=_required_text(
                    metadata, "semantic_type", source="governed item metadata"
                ),
                schema_version=_required_text(
                    metadata, "schema_version", source="governed item metadata"
                ),
                subject_identity=_required_text(
                    metadata, "subject_identity", source="governed item metadata"
                ),
                version_identity=_required_text(
                    metadata, "version_identity", source="governed item metadata"
                ),
                authority_mode=_required_text(
                    metadata, "authority_mode", source="governed item metadata"
                ),
                authority_scope=_required_text(
                    metadata, "authority_scope", source="governed item metadata"
                ),
                authoritative_source=_optional_text(metadata, "authoritative_source"),
                classification=_required_text(
                    metadata, "classification", source="governed item metadata"
                ),
                lifecycle_status=_optional_text(metadata, "lifecycle_status"),
                validation_status=_optional_text(metadata, "validation_status"),
                governed_admission_ref=_required_text(
                    metadata, "governed_admission_ref", source="governed item metadata"
                ),
                provenance_refs=tuple(value.strip() for value in provenance),
                source_release_sha=_required_text(
                    metadata, "source_release_sha", source="governed item metadata"
                ),
            )
        )
    return tuple(visible)


def _live_checkpoints(root: Path) -> tuple[LiveCheckpoint, ...]:
    checkpoints_root = root / "state" / "checkpoints"
    if not checkpoints_root.exists():
        raise UI1IntegrityError("checkpoint root is unavailable")
    if checkpoints_root.is_symlink() or not checkpoints_root.is_dir():
        raise UI1IntegrityError("checkpoint root is unsafe")
    entries = sorted(checkpoints_root.iterdir(), key=lambda path: path.name)
    for path in entries:
        if path.name.startswith(".") or path.is_symlink() or not path.is_file() or path.suffix != ".json":
            raise UI1IntegrityError("unexpected checkpoint-store entry")
    if len(entries) > MAX_VISIBLE_CHECKPOINTS:
        raise UI1IntegrityError(
            f"live checkpoint set exceeds UI1 bounded limit ({MAX_VISIBLE_CHECKPOINTS})"
        )

    visible: list[LiveCheckpoint] = []
    for path in entries:
        try:
            value = p703.verify_checkpoint(root, path)
        except p703.P703Error as exc:
            raise UI1IntegrityError("checkpoint integrity verification failed") from exc
        storage_ids = value.get("governed_storage_item_ids")
        if not isinstance(storage_ids, list) or not all(
            isinstance(item, str) and item.strip() for item in storage_ids
        ):
            raise UI1IntegrityError("checkpoint governed item references are invalid")
        visible.append(
            LiveCheckpoint(
                checkpoint_id=_required_text(value, "checkpoint_id", source="checkpoint"),
                execution_subject_identity=_required_text(
                    value, "execution_subject_identity", source="checkpoint"
                ),
                execution_version_identity=_required_text(
                    value, "execution_version_identity", source="checkpoint"
                ),
                classification=_required_text(value, "classification", source="checkpoint"),
                reason=_required_text(value, "reason", source="checkpoint"),
                governed_storage_item_ids=tuple(item.strip() for item in storage_ids),
            )
        )
    return tuple(visible)


def build_live_snapshot(
    root: Path,
    *,
    organization: Identity,
    principal: Identity,
    credential_id: str,
    credential_file: Path,
) -> LiveWorkspaceSnapshot:
    """Build one authorized, exact-release, live read-only snapshot.

    Authorization occurs before P7.03/P7.05 governed-state/health inspection, so
    failed identity/Organization/grant resolution cannot become a protected count
    or metadata disclosure channel.
    """

    root = root.expanduser().resolve()
    decision = _authorize(
        root,
        organization=organization,
        principal=principal,
        credential_id=credential_id,
        credential_file=credential_file,
    )
    workspace = _workspace_context(organization, principal)
    release_sha = _verify_exact_release(root)

    try:
        health = p705.classify_health(root)
    except (p705.P705Error, p704.P704Error, OSError, ValueError) as exc:
        raise UI1IntegrityError("runtime health is unavailable") from exc
    if health.state != "healthy":
        raise UI1IntegrityError("persistent runtime is not healthy")
    if health.release_sha != release_sha:
        raise UI1IntegrityError("persistent runtime release does not match the exact current release")

    items = _live_items(root)
    checkpoints = _live_checkpoints(root)
    return LiveWorkspaceSnapshot(
        workspace=workspace,
        runtime_root=root,
        release_sha=release_sha,
        health_state=health.state,
        health_code=health.code,
        health_detail=health.detail,
        heartbeat_age_seconds=health.heartbeat_age_seconds,
        items=items,
        checkpoints=checkpoints,
        access_grant_id=decision.grant_id,
    )


def _surface_for(item: LiveGovernedItem) -> set[WorkspaceDestination]:
    semantic = item.semantic_type.casefold()
    surfaces = {WorkspaceDestination.RECORDS}
    if "execution" in semantic or "workflow" in semantic:
        surfaces.add(WorkspaceDestination.EXECUTIONS)
    if "document" in semantic or "artifact" in semantic:
        surfaces.add(WorkspaceDestination.DOCUMENTS)
    if (
        "knowledge" in semantic
        or "memory" in semantic
        or "observation" in semantic
        or "learning" in semantic
    ):
        surfaces.add(WorkspaceDestination.KNOWLEDGE)
    return surfaces


def _missing(label: str) -> str:
    return (
        f'<span class="missing" data-evidence-state="missing">'
        f'{escape(label)}: not declared in retained metadata</span>'
    )


def _item_card(item: LiveGovernedItem) -> str:
    source = (
        f"Authoritative source: {escape(item.authoritative_source)}"
        if item.authoritative_source
        else _missing("Authoritative source")
    )
    lifecycle = (
        f"Lifecycle: {escape(item.lifecycle_status)}"
        if item.lifecycle_status
        else _missing("Lifecycle")
    )
    validation = (
        f"Validation: {escape(item.validation_status)}"
        if item.validation_status
        else _missing("Validation")
    )
    provenance = "".join(f"<li>{escape(ref)}</li>" for ref in item.provenance_refs)
    return (
        '<article class="record-card" data-authority="governed-source-metadata">'
        f"<h3>{escape(item.semantic_type)}</h3>"
        '<dl class="identity-pair">'
        "<div><dt>Subject</dt>"
        f"<dd>{escape(item.subject_identity)}</dd></div>"
        '<div class="exact"><dt>Exact Version</dt>'
        f"<dd>{escape(item.version_identity)}</dd></div>"
        "</dl>"
        '<div class="meta-grid">'
        f"<p>Schema: {escape(item.schema_version)}</p>"
        f"<p>Authority mode: {escape(item.authority_mode)}</p>"
        f"<p>Authority scope: {escape(item.authority_scope)}</p>"
        f"<p>{source}</p>"
        f"<p>Classification: {escape(item.classification)}</p>"
        f"<p>{lifecycle}</p>"
        f"<p>{validation}</p>"
        f"<p>Source release: <code>{escape(item.source_release_sha)}</code></p>"
        "</div>"
        '<details><summary>Evidence / provenance</summary>'
        f"<p>Governed admission: {escape(item.governed_admission_ref)}</p>"
        f"<ul>{provenance}</ul>"
        "<p>Payload bytes are intentionally not rendered in UI1.</p>"
        "</details>"
        "</article>"
    )


def _checkpoint_card(checkpoint: LiveCheckpoint) -> str:
    refs = "".join(
        f"<li>{escape(value)}</li>" for value in checkpoint.governed_storage_item_ids
    )
    return (
        '<article class="record-card checkpoint" data-authority="non-canonical-checkpoint">'
        "<h3>Recovery checkpoint</h3>"
        '<dl class="identity-pair">'
        "<div><dt>Execution Subject</dt>"
        f"<dd>{escape(checkpoint.execution_subject_identity)}</dd></div>"
        '<div class="exact"><dt>Exact Execution Version</dt>'
        f"<dd>{escape(checkpoint.execution_version_identity)}</dd></div>"
        "</dl>"
        f"<p>Checkpoint identity: {escape(checkpoint.checkpoint_id)}</p>"
        f"<p>Classification: {escape(checkpoint.classification)}</p>"
        f"<p>Reason: {escape(checkpoint.reason)}</p>"
        f"<details><summary>Governed item references</summary><ul>{refs}</ul></details>"
        "<p><strong>Non-authoritative recovery state.</strong> It does not replace canonical history.</p>"
        "</article>"
    )


def _empty_state(message: str) -> str:
    return (
        '<div class="empty" data-evidence-state="unavailable">'
        f"<p>{escape(message)}</p>"
        "<p>No hidden item metadata or inferred authority is substituted.</p>"
        "</div>"
    )


def _render_discover(snapshot: LiveWorkspaceSnapshot) -> str:
    counts = {
        destination: sum(destination in _surface_for(item) for item in snapshot.items)
        for destination in (
            WorkspaceDestination.RECORDS,
            WorkspaceDestination.EXECUTIONS,
            WorkspaceDestination.DOCUMENTS,
            WorkspaceDestination.KNOWLEDGE,
        )
    }
    cards = "".join(
        '<div class="metric">'
        f"<strong>{counts[destination]}</strong>"
        f"<span>{escape(destination.value)}</span></div>"
        for destination in counts
    )
    body = "".join(_item_card(item) for item in snapshot.items[:20])
    if not body:
        body = _empty_state("No authorized canonical governed items are currently retained.")
    return (
        "<section><h2>Discover</h2>"
        "<p>Live authorized discovery over retained canonical governed metadata. "
        "Counts are computed only after exact P7.04 authorization.</p>"
        f'<div class="metrics">{cards}</div>'
        "<h3>Recent bounded view</h3>"
        f"{body}</section>"
    )


def _render_records(snapshot: LiveWorkspaceSnapshot, destination: WorkspaceDestination) -> str:
    items = tuple(item for item in snapshot.items if destination in _surface_for(item))
    if not items:
        return (
            f"<section><h2>{escape(destination.value)}</h2>"
            + _empty_state(
                f"No authorized live items self-identify for the {destination.value} surface."
            )
            + "</section>"
        )
    projection_note = ""
    if destination is not WorkspaceDestination.RECORDS:
        projection_note = (
            "<p class=\"projection-note\">Surface grouping is a non-authoritative "
            "presentation projection over each retained semantic_type; it does not "
            "change canonical type or lifecycle.</p>"
        )
    return (
        f"<section><h2>{escape(destination.value)}</h2>{projection_note}"
        + "".join(_item_card(item) for item in items)
        + "</section>"
    )


def _render_evidence(snapshot: LiveWorkspaceSnapshot) -> str:
    item_evidence = "".join(
        '<article class="record-card evidence">'
        f"<h3>{escape(item.semantic_type)}</h3>"
        f"<p>Subject: {escape(item.subject_identity)}</p>"
        f"<p>Exact Version: {escape(item.version_identity)}</p>"
        f"<p>Governed admission: {escape(item.governed_admission_ref)}</p>"
        "<ul>"
        + "".join(f"<li>{escape(ref)}</li>" for ref in item.provenance_refs)
        + "</ul></article>"
        for item in snapshot.items
    )
    checkpoints = "".join(_checkpoint_card(value) for value in snapshot.checkpoints)
    if not item_evidence:
        item_evidence = _empty_state("No authorized canonical provenance records are retained.")
    if not checkpoints:
        checkpoints = _empty_state("No recovery checkpoints are currently retained.")
    return (
        "<section><h2>Evidence</h2>"
        "<p>Governed provenance is shown separately from non-authoritative recovery checkpoints.</p>"
        "<h3>Canonical governed provenance</h3>"
        f"{item_evidence}"
        "<h3>Recovery checkpoints</h3>"
        f"{checkpoints}</section>"
    )


def render_live_workspace_html(
    snapshot: LiveWorkspaceSnapshot,
    *,
    destination: WorkspaceDestination = WorkspaceDestination.DISCOVER,
) -> str:
    if not isinstance(snapshot, LiveWorkspaceSnapshot):
        raise ValueError("snapshot must be LiveWorkspaceSnapshot")
    if destination not in WORKSPACE_DESTINATIONS:
        raise ValueError("destination must be a workspace destination")

    if destination is WorkspaceDestination.DISCOVER:
        content = _render_discover(snapshot)
    elif destination is WorkspaceDestination.EVIDENCE:
        content = _render_evidence(snapshot)
    else:
        content = _render_records(snapshot, destination)

    nav = "".join(
        '<a href="/?view={key}"{current}>{label}</a>'.format(
            key=value.name.lower(),
            current=' aria-current="page"' if value is destination else "",
            label=escape(value.value),
        )
        for value in WORKSPACE_DESTINATIONS
    )
    age = (
        "unavailable"
        if snapshot.heartbeat_age_seconds is None
        else f"{snapshot.heartbeat_age_seconds:.1f}s"
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Arvectum OS — Live Governed Workspace</title>
<style>
:root {{ color-scheme: light dark; font-family: ui-sans-serif, system-ui, -apple-system, sans-serif; }}
body {{ margin: 0; background: Canvas; color: CanvasText; }}
header, main {{ max-width: 1180px; margin: auto; padding: 24px; }}
.context, .health, .record-card, .metric, .empty {{ border: 1px solid color-mix(in srgb, CanvasText 18%, transparent); border-radius: 14px; padding: 14px; }}
.context {{ display: grid; gap: 6px; margin-top: 12px; }}
.health {{ margin: 18px 0; }}
nav {{ display: flex; gap: 8px; flex-wrap: wrap; margin: 16px 0 24px; }}
nav a {{ padding: 9px 12px; border-radius: 999px; text-decoration: none; border: 1px solid currentColor; color: inherit; }}
nav a[aria-current="page"] {{ font-weight: 700; text-decoration: underline; }}
.metrics {{ display: grid; grid-template-columns: repeat(auto-fit,minmax(150px,1fr)); gap: 10px; margin: 14px 0 24px; }}
.metric {{ display: flex; justify-content: space-between; gap: 12px; }}
.record-card {{ margin: 12px 0; }}
.identity-pair {{ display: grid; grid-template-columns: repeat(auto-fit,minmax(240px,1fr)); gap: 10px; }}
.identity-pair > div {{ padding: 10px; border-radius: 10px; background: color-mix(in srgb, CanvasText 6%, transparent); }}
.identity-pair .exact {{ border: 1px solid currentColor; }}
dt {{ font-size: .8rem; font-weight: 700; text-transform: uppercase; }}
dd {{ margin: 4px 0 0; overflow-wrap: anywhere; }}
.meta-grid {{ display: grid; grid-template-columns: repeat(auto-fit,minmax(260px,1fr)); gap: 4px 18px; }}
.missing, .projection-note {{ opacity: .76; }}
code {{ overflow-wrap: anywhere; }}
footer {{ max-width: 1180px; margin: 0 auto; padding: 0 24px 32px; opacity: .8; }}
</style>
</head>
<body>
<header>
<h1>Arvectum OS — Live Governed Workspace</h1>
<p><strong>Read-only / non-authoritative presentation.</strong> This interface grants no Organizational Authority, approval, or canonical mutation path.</p>
<div class="context" aria-label="Current governed context">
<span>Organization: {escape(snapshot.organization_id)}</span>
<span>Actor: {escape(snapshot.actor_id)} (human / attributable)</span>
<span>Exact runtime release: <code>{escape(snapshot.release_sha)}</code></span>
</div>
<div class="health" aria-label="Runtime health">
<strong>Runtime health: {escape(snapshot.health_state)}</strong>
<span> · {escape(snapshot.health_code)} · heartbeat age {escape(age)}</span>
<p>{escape(snapshot.health_detail)}</p>
</div>
<nav aria-label="Workspace">{nav}</nav>
</header>
<main data-presentation-authority="non-authoritative">{content}</main>
<footer>
<p>Subject and Exact Version are intentionally distinct. Missing lifecycle/source/validation metadata is shown as missing rather than inferred. Governed-test fixtures are excluded from live surfaces.</p>
</footer>
</body>
</html>"""


def render_blocked_html() -> str:
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Workspace unavailable</title></head>
<body><main data-workspace-state="blocked">
<h1>Workspace unavailable</h1>
<p role="alert">The governed workspace cannot be opened in the current context.</p>
<p>Governed content, protected counts, and protected identifiers are not exposed.</p>
</main></body></html>"""


def _destination_from_path(path: str) -> WorkspaceDestination:
    parsed = urlsplit(path)
    if parsed.path != "/":
        raise UI1BoundaryError("unknown private workspace path")
    values = parse_qs(parsed.query, keep_blank_values=True)
    if set(values) - {"view"}:
        raise UI1BoundaryError("unsupported workspace query")
    requested = values.get("view", ["discover"])
    if len(requested) != 1:
        raise UI1BoundaryError("ambiguous workspace view")
    key = requested[0].strip().lower()
    mapping = {value.name.lower(): value for value in WORKSPACE_DESTINATIONS}
    if key not in mapping:
        raise UI1BoundaryError("unknown workspace view")
    return mapping[key]


def _security_headers(handler: BaseHTTPRequestHandler) -> None:
    handler.send_header("Cache-Control", "no-store, max-age=0")
    handler.send_header("Pragma", "no-cache")
    handler.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'")
    handler.send_header("Referrer-Policy", "no-referrer")
    handler.send_header("X-Content-Type-Options", "nosniff")
    handler.send_header("X-Frame-Options", "DENY")


def _write_html(handler: BaseHTTPRequestHandler, status: HTTPStatus, body: str) -> None:
    encoded = body.encode("utf-8")
    handler.send_response(status.value)
    _security_headers(handler)
    handler.send_header("Content-Type", "text/html; charset=utf-8")
    handler.send_header("Content-Length", str(len(encoded)))
    handler.end_headers()
    if handler.command != "HEAD":
        handler.wfile.write(encoded)


def make_server(
    *,
    host: str,
    port: int,
    root: Path,
    organization: Identity,
    principal: Identity,
    credential_id: str,
    credential_file: Path,
) -> ThreadingHTTPServer:
    host = _verify_loopback_host(host)
    if not isinstance(port, int) or port < 0 or port > 65535:
        raise UI1BoundaryError("port must be between 0 and 65535")

    build_live_snapshot(
        root,
        organization=organization,
        principal=principal,
        credential_id=credential_id,
        credential_file=credential_file,
    )

    class Handler(BaseHTTPRequestHandler):
        server_version = "ArvectumOS-UI1"
        sys_version = ""

        def log_message(self, _format: str, *_args: object) -> None:
            return

        def _read(self) -> None:
            try:
                destination = _destination_from_path(self.path)
                snapshot = build_live_snapshot(
                    root,
                    organization=organization,
                    principal=principal,
                    credential_id=credential_id,
                    credential_file=credential_file,
                )
                body = render_live_workspace_html(snapshot, destination=destination)
            except UI1AccessDenied:
                _write_html(self, HTTPStatus.FORBIDDEN, render_blocked_html())
                return
            except (UI1IntegrityError, UI1BoundaryError, p703.P703Error, p704.P704Error, p705.P705Error, p706.P706Error, OSError, ValueError):
                _write_html(self, HTTPStatus.SERVICE_UNAVAILABLE, render_blocked_html())
                return
            _write_html(self, HTTPStatus.OK, body)

        def do_GET(self) -> None:  # noqa: N802
            self._read()

        def do_HEAD(self) -> None:  # noqa: N802
            self._read()

        def _reject_mutation(self) -> None:
            _write_html(self, HTTPStatus.METHOD_NOT_ALLOWED, render_blocked_html())

        do_POST = _reject_mutation
        do_PUT = _reject_mutation
        do_PATCH = _reject_mutation
        do_DELETE = _reject_mutation

    return ThreadingHTTPServer((host, port), Handler)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Arvectum OS P7.06-UI1 live read-only governed workspace"
    )
    parser.add_argument("--runtime-root", required=True)
    parser.add_argument("--organization", required=True, help="exact Organization identity value")
    parser.add_argument("--principal", required=True, help="exact human Principal identity value")
    parser.add_argument("--credential-id", required=True)
    parser.add_argument("--credential-file", required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        host = _verify_loopback_host(args.host)
        organization = Identity("organization", args.organization, "platform")
        principal = Identity("principal", args.principal, organization.value)
        server = make_server(
            host=host,
            port=args.port,
            root=Path(args.runtime_root),
            organization=organization,
            principal=principal,
            credential_id=args.credential_id,
            credential_file=Path(args.credential_file),
        )
    except (UI1Error, p703.P703Error, p704.P704Error, p705.P705Error, p706.P706Error, OSError, ValueError) as exc:
        print(f"P7.06-UI1 FAIL: {exc}", file=sys.stderr)
        return 1

    actual_host, actual_port = server.server_address[:2]
    print(f"P7.06-UI1 READY http://{actual_host}:{actual_port}/")
    try:
        server.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
