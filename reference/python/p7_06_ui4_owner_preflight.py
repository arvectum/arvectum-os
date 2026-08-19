#!/usr/bin/env python3
"""P7.06-UI4 — first real owner interaction preflight.

This is a bounded, owner-operated, preflight-only bridge over the already-retained
P7.03 governed document used by UI1.  It deliberately does not manufacture a
GovernedInteractionCase or canonical successor merely to make a button succeed.

The bridge:
* reuses UI1 exact-release/health/read authorization and UI2 exact local human
  interaction access;
* selects one real retained ``platform.document`` and re-verifies its immutable
  P7.03 manifest/payload/checkpoint continuity;
* shows exact Subject/Version, External Reference authority, execution/event and
  provenance/reconstruction evidence;
* keeps technical workspace access distinct from the four RFC-0005 action gates;
* leaves action-specific Authorization, Organizational Authority, Data Governance
  and Consequential Approval as Waiting because UI4 supplies none of them;
* lets the owner submit only a bounded preflight request, which re-evaluates all
  evidence and writes minimized owner-local non-canonical proof evidence;
* performs no canonical mutation, product/external effect, authority delegation or
  consequential approval.

No public/stable route, API, session protocol or browser-support contract is
created by this proof adapter.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from html import escape
from http import HTTPStatus
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import parse_qs

from arvectum_os_ref.identity import Identity

import p7_03_durable_state as p703
import p7_06_ui1_live_workspace as ui1
import p7_06_ui2_governed_interaction as ui2


UTC = timezone.utc
PREFLIGHT_PATH = "/ui4/preflight"
RUN_PATH = "/ui4/preflight/run"
PREFLIGHT_ID = "p7-06-ui4:first-real-owner-preflight"
TARGET_SEMANTIC_TYPE = "platform.document"
TARGET_AUTHORITY_MODE = "External Reference"
TARGET_PAYLOAD_SCHEMA = "arvectum.p7_06.ui1-real-governed-document/1"
EVIDENCE_SCHEMA = "arvectum.p7_06.ui4-owner-preflight-evidence/1"
MAX_PAYLOAD_BYTES = 128 * 1024
MAX_FORM_BYTES = 4096
EVIDENCE_BASENAME = "p7-06-ui4-owner-preflight-last.json"


class UI4Error(RuntimeError):
    """Base UI4 proof error."""


class UI4IntegrityError(UI4Error):
    """Real retained state or proof continuity failed closed."""


class UI4BoundaryError(UI4Error):
    """The bounded owner-preflight boundary would be crossed."""


@dataclass(frozen=True, slots=True)
class UI4GateView:
    name: str
    state: str
    basis: str


@dataclass(frozen=True, slots=True)
class UI4OwnerPreflight:
    release_sha: str
    organization_id: str
    actor_id: str
    storage_item_id: str
    subject_identity: str
    version_identity: str
    semantic_type: str
    authority_mode: str
    authority_scope: str
    authoritative_source: str
    execution_subject: str
    execution_version: str
    event_version: str
    checkpoint_id: str
    provenance_refs: tuple[str, ...]
    validation_status: str
    gates: tuple[UI4GateView, ...]
    outcome: str = "Waiting"
    technical_interaction_access: str = "PASS"
    presentation_authority: str = "non-authoritative"
    canonical_mutation_requested: bool = False
    external_effect_requested: bool = False


@dataclass(frozen=True, slots=True)
class UI4EvidenceReceipt:
    path: Path
    sha256: str
    preflight: UI4OwnerPreflight


def _required_text(value: Mapping[str, Any], key: str, *, source: str) -> str:
    item = value.get(key)
    if not isinstance(item, str) or not item.strip():
        raise UI4IntegrityError(f"{source} has no valid {key}")
    return item.strip()


def _load_payload(item_dir: Path) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    manifest = p703.verify_item(item_dir)
    payload_path = item_dir / "payload.bin"
    if payload_path.is_symlink() or not payload_path.is_file():
        raise UI4IntegrityError("retained governed payload is unavailable")
    if payload_path.stat().st_size <= 0 or payload_path.stat().st_size > MAX_PAYLOAD_BYTES:
        raise UI4IntegrityError("retained governed payload is outside the bounded UI4 size")
    try:
        payload = json.loads(payload_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise UI4IntegrityError("retained governed payload is not readable minimized JSON") from exc
    if not isinstance(payload, dict):
        raise UI4IntegrityError("retained governed payload must be a JSON object")
    metadata = manifest.get("metadata")
    if not isinstance(metadata, dict):
        raise UI4IntegrityError("retained governed metadata is unavailable")
    return metadata, payload


def _select_real_document(
    root: Path,
    snapshot: ui1.LiveWorkspaceSnapshot,
) -> tuple[ui1.LiveGovernedItem, Mapping[str, Any], Mapping[str, Any]]:
    items_root = root / "state" / "governed" / "items"
    matches: list[tuple[ui1.LiveGovernedItem, Mapping[str, Any], Mapping[str, Any]]] = []
    for item in snapshot.items:
        if item.semantic_type != TARGET_SEMANTIC_TYPE or item.authority_mode != TARGET_AUTHORITY_MODE:
            continue
        item_dir = items_root / item.storage_item_id
        metadata, payload = _load_payload(item_dir)
        if payload.get("schema") != TARGET_PAYLOAD_SCHEMA:
            continue
        matches.append((item, metadata, payload))
    if len(matches) != 1:
        raise UI4IntegrityError(
            "UI4 bounded proof requires exactly one retained UI1 real governed document"
        )
    return matches[0]


def _validate_real_chain(
    snapshot: ui1.LiveWorkspaceSnapshot,
    item: ui1.LiveGovernedItem,
    metadata: Mapping[str, Any],
    payload: Mapping[str, Any],
) -> tuple[str, str, str, ui1.LiveCheckpoint]:
    exact_pairs = (
        ("subject_identity", item.subject_identity),
        ("version_identity", item.version_identity),
        ("semantic_type", item.semantic_type),
        ("schema_version", item.schema_version),
        ("authority_mode", item.authority_mode),
        ("authority_scope", item.authority_scope),
    )
    for key, expected in exact_pairs:
        if payload.get(key) != expected:
            raise UI4IntegrityError(f"retained payload/manifest continuity mismatch: {key}")
    if metadata.get("subject_identity") != item.subject_identity:
        raise UI4IntegrityError("retained metadata lost exact Subject continuity")
    if metadata.get("version_identity") != item.version_identity:
        raise UI4IntegrityError("retained metadata lost exact Version continuity")
    if metadata.get("governed_admission_ref") != payload.get("event_version"):
        raise UI4IntegrityError("retained admission Event continuity mismatch")
    if payload.get("external_actions") is not False:
        raise UI4IntegrityError("retained UI4 source claims an external action")
    if payload.get("raw_document_bytes_included") is not False:
        raise UI4IntegrityError("retained UI4 source unexpectedly contains raw document bytes")
    if payload.get("reusable_secret_included") is not False:
        raise UI4IntegrityError("retained UI4 source unexpectedly contains reusable secret material")

    execution_subject = _required_text(payload, "execution_subject", source="retained payload")
    execution_version = _required_text(payload, "execution_version", source="retained payload")
    event_version = _required_text(payload, "event_version", source="retained payload")
    provenance = set(item.provenance_refs)
    for exact in (execution_subject, execution_version, event_version):
        if exact not in provenance:
            raise UI4IntegrityError("retained provenance chain lost exact execution/event evidence")

    checkpoints = tuple(
        checkpoint
        for checkpoint in snapshot.checkpoints
        if item.storage_item_id in checkpoint.governed_storage_item_ids
        and checkpoint.execution_subject_identity == execution_subject
        and checkpoint.execution_version_identity == execution_version
    )
    if len(checkpoints) != 1:
        raise UI4IntegrityError(
            "exact retained execution/checkpoint reconstruction continuity is ambiguous"
        )
    return execution_subject, execution_version, event_version, checkpoints[0]


def build_owner_preflight(
    root: Path,
    *,
    organization: Identity,
    principal: Identity,
    credential_id: str,
    credential_file: Path,
) -> UI4OwnerPreflight:
    """Re-evaluate one real owner preflight without constructing a mutation case."""
    root = root.expanduser().resolve()
    snapshot = ui1.build_live_snapshot(
        root,
        organization=organization,
        principal=principal,
        credential_id=credential_id,
        credential_file=credential_file,
    )
    technical = ui2._authorize_interaction(
        root,
        organization=organization,
        principal=principal,
        credential_id=credential_id,
        credential_file=credential_file,
    )
    if not technical.allowed or technical.principal_kind != "human":
        raise UI4BoundaryError("exact UI2 human/local technical interaction access is required")
    if technical.organizational_authority_satisfied or technical.consequential_approval_satisfied:
        raise UI4BoundaryError("technical interaction access must not become authority or approval")

    item, metadata, payload = _select_real_document(root, snapshot)
    execution_subject, execution_version, event_version, checkpoint = _validate_real_chain(
        snapshot, item, metadata, payload
    )
    authoritative_source = item.authoritative_source
    if not isinstance(authoritative_source, str) or not authoritative_source.strip():
        raise UI4IntegrityError("real retained document has no authoritative source")
    validation_status = item.validation_status
    if not isinstance(validation_status, str) or "CAP-004 reconstruction complete" not in validation_status:
        raise UI4IntegrityError("real retained document lacks retained CAP-004 reconstruction evidence")

    # P7.04/UI3 technical access is deliberately outside these RFC-0005 action
    # gates.  No action-specific decision evidence is manufactured by UI4.
    gates = (
        UI4GateView(
            "Authorization",
            "Waiting",
            "No action-specific authorization decision supplied; workspace.interact is technical access only.",
        ),
        UI4GateView(
            "Organizational Authority",
            "Waiting",
            "UI3/P7.04 supply no Organizational Authority and UI4 introduces no delegation.",
        ),
        UI4GateView(
            "Data Governance",
            "Waiting",
            "No new purpose-specific data-governance decision is supplied for a canonical change.",
        ),
        UI4GateView(
            "Consequential Approval",
            "Waiting",
            "The browser/session/button is not approval; no consequential approval is supplied.",
        ),
    )
    return UI4OwnerPreflight(
        release_sha=snapshot.release_sha,
        organization_id=snapshot.organization_id,
        actor_id=snapshot.actor_id,
        storage_item_id=item.storage_item_id,
        subject_identity=item.subject_identity,
        version_identity=item.version_identity,
        semantic_type=item.semantic_type,
        authority_mode=item.authority_mode,
        authority_scope=item.authority_scope,
        authoritative_source=authoritative_source.strip(),
        execution_subject=execution_subject,
        execution_version=execution_version,
        event_version=event_version,
        checkpoint_id=checkpoint.checkpoint_id,
        provenance_refs=item.provenance_refs,
        validation_status=validation_status,
        gates=gates,
    )


def _document(preflight: UI4OwnerPreflight, *, csrf_token: str, ran: bool) -> str:
    gate_rows = "".join(
        "<tr>"
        f"<th>{escape(row.name)}</th><td>{escape(row.state)}</td><td>{escape(row.basis)}</td>"
        "</tr>"
        for row in preflight.gates
    )
    provenance = "".join(f"<li>{escape(value)}</li>" for value in preflight.provenance_refs)
    result = (
        '<p role="status"><strong>Preflight executed: WAITING / fail-closed.</strong> '
        "No canonical mutation or external effect was requested.</p>"
        if ran
        else ""
    )
    form = (
        f'<form method="post" action="{RUN_PATH}">'
        f'<input type="hidden" name="preflight_id" value="{escape(PREFLIGHT_ID)}">'
        f'<input type="hidden" name="csrf" value="{escape(csrf_token)}">'
        '<button type="submit">Run governed preflight</button>'
        "</form>"
    )
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Arvectum OS — First owner preflight</title></head>
<body><header><h1>P7.06-UI4 — First real owner preflight</h1>
<p><strong>Private / owner-operated / non-authoritative.</strong> This surface grants no authority or approval.</p>
<p>Organization: {escape(preflight.organization_id)}<br>
Actor: {escape(preflight.actor_id)} (human / attributable)<br>
Exact runtime release: <code>{escape(preflight.release_sha)}</code><br>
Technical interaction access: {escape(preflight.technical_interaction_access)}</p>
<nav><a href="/?view=records">Records</a> · <a href="/?view=executions">Executions</a> · <a href="/?view=evidence">Evidence</a> · <a href="/?view=documents">Documents</a> · <a href="/?view=knowledge">Knowledge</a></nav></header>
<main data-presentation-authority="non-authoritative" data-ui4-outcome="waiting">
{result}
<section><h2>Exact retained governed source</h2>
<p>Semantic type: {escape(preflight.semantic_type)}<br>
Subject: <code>{escape(preflight.subject_identity)}</code><br>
Version: <code>{escape(preflight.version_identity)}</code><br>
Authority: {escape(preflight.authority_mode)} / {escape(preflight.authority_scope)}<br>
Authoritative source: {escape(preflight.authoritative_source)}<br>
Storage locator: <code>{escape(preflight.storage_item_id)}</code></p></section>
<section><h2>Execution / Event / reconstruction continuity</h2>
<p>Execution Subject: <code>{escape(preflight.execution_subject)}</code><br>
Execution Version: <code>{escape(preflight.execution_version)}</code><br>
Admission Event Version: <code>{escape(preflight.event_version)}</code><br>
Recovery checkpoint: <code>{escape(preflight.checkpoint_id)}</code><br>
Validation: {escape(preflight.validation_status)}</p>
<ul>{provenance}</ul></section>
<section><h2>Action gate preflight</h2>
<p>Technical P7.04 access is not an RFC-0005 action decision. UI4 supplies no action-specific gate evidence.</p>
<table><thead><tr><th>Gate</th><th>State</th><th>Basis</th></tr></thead><tbody>{gate_rows}</tbody></table>
<p><strong>Outcome: Waiting.</strong> No action request is available until independently governed decision evidence exists.</p>
{form}</section></main>
<footer><p>Preflight-only proof adapter. No public/stable route or API contract.</p></footer></body></html>"""


def render_owner_preflight_html(
    preflight: UI4OwnerPreflight,
    *,
    csrf_token: str,
    ran: bool = False,
) -> str:
    if not isinstance(preflight, UI4OwnerPreflight):
        raise UI4BoundaryError("typed UI4 preflight required")
    if not isinstance(csrf_token, str) or not csrf_token:
        raise UI4BoundaryError("bounded UI4 CSRF token required")
    return _document(preflight, csrf_token=csrf_token, ran=ran)


def read_run_form(handler: Any) -> Mapping[str, str]:
    content_type = handler.headers.get("Content-Type", "")
    if content_type.split(";", 1)[0].strip().lower() != "application/x-www-form-urlencoded":
        raise UI4BoundaryError("UI4 accepts only bounded form submissions")
    raw_length = handler.headers.get("Content-Length")
    try:
        length = int(raw_length or "")
    except ValueError as exc:
        raise UI4BoundaryError("invalid UI4 form length") from exc
    if length <= 0 or length > MAX_FORM_BYTES:
        raise UI4BoundaryError("UI4 form is outside the bounded size")
    try:
        text = handler.rfile.read(length).decode("utf-8")
        values = parse_qs(text, keep_blank_values=True, strict_parsing=True)
    except (UnicodeDecodeError, ValueError) as exc:
        raise UI4BoundaryError("malformed UI4 form") from exc
    if set(values) != {"preflight_id", "csrf"} or any(len(items) != 1 for items in values.values()):
        raise UI4BoundaryError("UI4 browser input may contain only preflight_id and csrf")
    result = {key: items[0] for key, items in values.items()}
    if result["preflight_id"] != PREFLIGHT_ID or not result["csrf"]:
        raise UI4BoundaryError("UI4 preflight continuity mismatch")
    return result


def _evidence_path(root: Path) -> Path:
    return root.expanduser().resolve() / "evidence" / EVIDENCE_BASENAME


def _atomic_owner_json(path: Path, value: Mapping[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if os.name != "nt":
        os.chmod(path.parent, 0o700)
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    digest = hashlib.sha256(payload).hexdigest()
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        if os.name != "nt":
            os.fchmod(fd, 0o600)
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
        if os.name != "nt":
            os.chmod(path, 0o600)
    finally:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
    return digest


def record_browser_preflight(root: Path, preflight: UI4OwnerPreflight) -> UI4EvidenceReceipt:
    if any(row.state != "Waiting" for row in preflight.gates):
        raise UI4BoundaryError("UI4 proof may record only the declared fail-closed Waiting preflight")
    value = {
        "schema": EVIDENCE_SCHEMA,
        "recorded_at": datetime.now(UTC).isoformat(),
        "preflight_id": PREFLIGHT_ID,
        "release_sha": preflight.release_sha,
        "organization_id": preflight.organization_id,
        "actor_id": preflight.actor_id,
        "storage_item_id": preflight.storage_item_id,
        "subject_identity": preflight.subject_identity,
        "version_identity": preflight.version_identity,
        "execution_subject": preflight.execution_subject,
        "execution_version": preflight.execution_version,
        "event_version": preflight.event_version,
        "checkpoint_id": preflight.checkpoint_id,
        "gate_states": {row.name: row.state for row in preflight.gates},
        "technical_interaction_access": True,
        "browser_preflight_post_observed": True,
        "organizational_authority_provided": False,
        "consequential_approval_provided": False,
        "canonical_mutation_requested": False,
        "canonical_mutation_performed": False,
        "product_or_external_effect_requested": False,
        "product_or_external_effect_performed": False,
        "reusable_secret_recorded": False,
        "browser_session_recorded": False,
    }
    path = _evidence_path(root)
    digest = _atomic_owner_json(path, value)
    return UI4EvidenceReceipt(path=path, sha256=digest, preflight=preflight)


def write_html(handler: Any, status: HTTPStatus, body: str) -> None:
    encoded = body.encode("utf-8")
    handler.send_response(status.value)
    ui2._security_headers(handler)
    handler.send_header("Content-Type", "text/html; charset=utf-8")
    handler.send_header("Content-Length", str(len(encoded)))
    handler.end_headers()
    if handler.command != "HEAD":
        handler.wfile.write(encoded)
