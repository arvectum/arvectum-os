"""P7.06-UI2 private loopback adapter for governed interaction/preflight.

The adapter extends the UI1 read-only boundary with one narrowly scoped request
entry point.  It does not accept candidate records, gate decisions, authority,
approval, reconstruction evidence or retry semantics from the browser.  Trusted
in-process providers supply a typed GovernedInteractionCase and optional
CAP-004 AuditReconstructionView; every request reuses UI1 exact-release and read
authorization checks, while POST additionally requires its own P7.04 human/local
grant, same-origin/CSRF checks, and a fresh governed preflight.

No public/stable route, session, browser, SDK or frontend contract is created.
P7.06-UI3 remains responsible for persistent private operator process/access.
"""

from __future__ import annotations

import hmac
import secrets
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Callable, Mapping
from urllib.parse import parse_qs, urlsplit

from arvectum_os_ref.audit_reconstruction_support import AuditReconstructionView
from arvectum_os_ref.governed_interaction_preflight import (
    GovernedInteractionBlocked,
    GovernedInteractionCase,
    build_governed_interaction_preflight,
    execute_governed_interaction,
    render_governed_interaction_preflight_html,
    render_governed_interaction_result_html,
)
from arvectum_os_ref.governed_interaction_reconstruction import (
    build_source_reconstruction_view,
    render_source_reconstruction_html,
)
from arvectum_os_ref.governed_interaction_runtime_outcomes import (
    inspect_consequential_outcome_evidence,
    render_consequential_outcome_evidence_html,
)
from arvectum_os_ref.identity import Identity

import p7_04_persistent_access as p704
import p7_06_ui1_live_workspace as ui1


INTERACTION_OPERATION = "workspace.interact"
INTERACTION_RESOURCE = "workspace:p7-06-ui2"
INTERACTION_ACCESS_PATH = "local"
MAX_FORM_BYTES = 4096
MAX_INTERACTION_ID_CHARS = 128

InteractionProvider = Callable[[str], GovernedInteractionCase | None]
ReconstructionProvider = Callable[[str], AuditReconstructionView | None]


class UI2Error(RuntimeError):
    """Base P7.06-UI2 adapter error."""


class UI2AccessDenied(UI2Error):
    """Technical UI access failed before protected interaction disclosure."""


class UI2BoundaryError(UI2Error):
    """Private/same-origin/browser-input boundary would be crossed."""


def _authorize_interaction(
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
        operation=INTERACTION_OPERATION,
        resource=INTERACTION_RESOURCE,
        access_path=INTERACTION_ACCESS_PATH,
    )
    if not decision.allowed or decision.principal_kind != "human":
        raise UI2AccessDenied("governed interaction is unavailable")
    if decision.organizational_authority_satisfied or decision.consequential_approval_satisfied:
        raise UI2BoundaryError(
            "technical workspace access must not satisfy Organizational Authority or approval"
        )
    if not isinstance(decision.grant_id, str) or not decision.grant_id:
        raise UI2BoundaryError("allowed interaction access has no attributable exact grant")
    return decision


def _provider_case(
    provider: InteractionProvider,
    interaction_id: str,
) -> GovernedInteractionCase | None:
    if not isinstance(interaction_id, str):
        raise UI2BoundaryError("interaction identifier must be text")
    interaction_id = interaction_id.strip()
    if not interaction_id or len(interaction_id) > MAX_INTERACTION_ID_CHARS:
        raise UI2BoundaryError("interaction identifier is outside the bounded UI2 shape")
    try:
        case = provider(interaction_id)
    except Exception as exc:
        raise UI2BoundaryError("trusted interaction provider is unavailable") from exc
    if case is None:
        return None
    if not isinstance(case, GovernedInteractionCase):
        raise UI2BoundaryError("trusted interaction provider returned invalid evidence")
    if case.interaction_id != interaction_id:
        raise UI2BoundaryError("trusted interaction identifier continuity mismatch")
    return case


def _provider_reconstruction(
    provider: ReconstructionProvider | None,
    interaction_id: str,
) -> AuditReconstructionView | None:
    if provider is None:
        return None
    try:
        view = provider(interaction_id)
    except Exception as exc:
        raise UI2BoundaryError("trusted reconstruction provider is unavailable") from exc
    if view is not None and not isinstance(view, AuditReconstructionView):
        raise UI2BoundaryError("trusted reconstruction provider returned invalid evidence")
    return view


def _interaction_id_from_get(path: str) -> str:
    parsed = urlsplit(path)
    if parsed.path != "/interaction":
        raise UI2BoundaryError("unknown interaction path")
    values = parse_qs(parsed.query, keep_blank_values=True)
    if set(values) != {"id"}:
        raise UI2BoundaryError("interaction query must contain exactly one id")
    ids = values["id"]
    if len(ids) != 1:
        raise UI2BoundaryError("interaction query is ambiguous")
    interaction_id = ids[0].strip()
    if not interaction_id or len(interaction_id) > MAX_INTERACTION_ID_CHARS:
        raise UI2BoundaryError("interaction identifier is outside the bounded UI2 shape")
    return interaction_id


def _read_form(handler: BaseHTTPRequestHandler) -> Mapping[str, str]:
    content_type = handler.headers.get("Content-Type", "")
    if content_type.split(";", 1)[0].strip().lower() != "application/x-www-form-urlencoded":
        raise UI2BoundaryError("UI2 accepts only bounded form submissions")
    raw_length = handler.headers.get("Content-Length")
    try:
        length = int(raw_length or "")
    except ValueError as exc:
        raise UI2BoundaryError("invalid form content length") from exc
    if length <= 0 or length > MAX_FORM_BYTES:
        raise UI2BoundaryError("form size is outside the bounded UI2 limit")
    payload = handler.rfile.read(length)
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise UI2BoundaryError("form must be UTF-8") from exc
    try:
        values = parse_qs(text, keep_blank_values=True, strict_parsing=True)
    except ValueError as exc:
        raise UI2BoundaryError("malformed form encoding") from exc
    if set(values) != {"interaction_id", "csrf"}:
        raise UI2BoundaryError("browser submission may contain only interaction_id and csrf")
    if any(len(items) != 1 for items in values.values()):
        raise UI2BoundaryError("browser submission fields must be singular")
    return {key: items[0] for key, items in values.items()}


def _expected_origin(handler: BaseHTTPRequestHandler) -> str:
    host, port = handler.server.server_address[:2]
    return f"http://{host}:{port}"


def _require_loopback_host(handler: BaseHTTPRequestHandler) -> None:
    host, port = handler.server.server_address[:2]
    expected_host = f"{host}:{port}"
    if handler.headers.get("Host") != expected_host:
        raise UI2BoundaryError("loopback Host boundary mismatch")


def _require_same_origin(handler: BaseHTTPRequestHandler) -> None:
    _require_loopback_host(handler)
    if handler.headers.get("Origin") != _expected_origin(handler):
        raise UI2BoundaryError("same-origin POST is required")


def _security_headers(handler: BaseHTTPRequestHandler) -> None:
    handler.send_header("Cache-Control", "no-store, max-age=0")
    handler.send_header("Pragma", "no-cache")
    handler.send_header(
        "Content-Security-Policy",
        "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'",
    )
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


def _blocked_html(message: str = "Governed interaction is unavailable.") -> str:
    from html import escape

    return (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<title>Governed interaction unavailable</title></head>"
        '<body><main data-interaction-state="blocked">'
        "<h1>Governed interaction unavailable</h1>"
        f'<p role="alert">{escape(message)}</p>'
        "<p>Protected Subject, Version, gate evidence and action details are not exposed.</p>"
        "</main></body></html>"
    )


def _interaction_document(snapshot: ui1.LiveWorkspaceSnapshot, body: str) -> str:
    from html import escape

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Arvectum OS — Governed Interaction</title>
</head>
<body>
<header>
<h1>Arvectum OS — Governed Interaction</h1>
<p><strong>Private / non-authoritative preflight.</strong> Technical access, UI state and buttons grant no authority or approval.</p>
<p>Organization: {escape(snapshot.organization_id)}<br>
Actor: {escape(snapshot.actor_id)} (human / attributable)<br>
Exact runtime release: <code>{escape(snapshot.release_sha)}</code><br>
Runtime health: {escape(snapshot.health_state)}</p>
<p><a href="/?view=executions">Back to read-only Executions</a></p>
</header>
<main data-presentation-authority="non-authoritative">{body}</main>
<footer><p>P7.06-UI2 private reversible adapter. No public/stable route or API contract.</p></footer>
</body>
</html>"""


def make_server(
    *,
    host: str,
    port: int,
    root: Path,
    organization: Identity,
    principal: Identity,
    credential_id: str,
    credential_file: Path,
    interaction_provider: InteractionProvider,
    reconstruction_provider: ReconstructionProvider | None = None,
) -> ThreadingHTTPServer:
    """Build the bounded UI2 server; persistent supervision remains P7.06-UI3."""

    host = ui1._verify_loopback_host(host)
    if not isinstance(port, int) or port < 0 or port > 65535:
        raise UI2BoundaryError("port must be between 0 and 65535")
    if not callable(interaction_provider):
        raise UI2BoundaryError("interaction_provider must be callable")
    if reconstruction_provider is not None and not callable(reconstruction_provider):
        raise UI2BoundaryError("reconstruction_provider must be callable when supplied")

    # Preserve UI1 exact-release/health/read-access startup invariants.
    ui1.build_live_snapshot(
        root,
        organization=organization,
        principal=principal,
        credential_id=credential_id,
        credential_file=credential_file,
    )
    csrf_token = secrets.token_urlsafe(32)

    class Handler(BaseHTTPRequestHandler):
        server_version = "ArvectumOS-UI2"
        sys_version = ""

        def log_message(self, _format: str, *_args: object) -> None:
            return

        def _snapshot(self) -> ui1.LiveWorkspaceSnapshot:
            return ui1.build_live_snapshot(
                root,
                organization=organization,
                principal=principal,
                credential_id=credential_id,
                credential_file=credential_file,
            )

        def _interaction_access(self) -> p704.AccessDecision:
            return _authorize_interaction(
                root,
                organization=organization,
                principal=principal,
                credential_id=credential_id,
                credential_file=credential_file,
            )

        def _reconstruction_html(
            self,
            case: GovernedInteractionCase,
            interaction_id: str,
        ) -> str:
            audit_view = _provider_reconstruction(reconstruction_provider, interaction_id)
            view = build_source_reconstruction_view(
                organization=case.organization,
                source_record=case.source_record,
                audit_view=audit_view,
            )
            return render_source_reconstruction_html(view)

        def _outcome_evidence_html(self, case: GovernedInteractionCase) -> str:
            execution = case.execution_lineage.head()
            evidence = inspect_consequential_outcome_evidence(
                case.runtime_state,
                execution_subject_id=execution.execution_subject_id,
            )
            return render_consequential_outcome_evidence_html(evidence)

        def _get(self) -> None:
            parsed = urlsplit(self.path)
            try:
                _require_loopback_host(self)
                snapshot = self._snapshot()
                if parsed.path == "/":
                    destination = ui1._destination_from_path(self.path)
                    _write_html(
                        self,
                        HTTPStatus.OK,
                        ui1.render_live_workspace_html(snapshot, destination=destination),
                    )
                    return
                if parsed.path != "/interaction":
                    raise UI2BoundaryError("unknown private workspace path")
                self._interaction_access()
                interaction_id = _interaction_id_from_get(self.path)
                case = _provider_case(interaction_provider, interaction_id)
                if case is None:
                    _write_html(self, HTTPStatus.NOT_FOUND, _blocked_html())
                    return
                preflight = build_governed_interaction_preflight(snapshot.workspace, case=case)
                body = render_governed_interaction_preflight_html(
                    preflight,
                    interaction_id=interaction_id,
                    csrf_token=csrf_token,
                )
                if not isinstance(preflight, GovernedInteractionBlocked):
                    body += self._reconstruction_html(case, interaction_id)
                    body += self._outcome_evidence_html(case)
                _write_html(self, HTTPStatus.OK, _interaction_document(snapshot, body))
            except ui1.UI1AccessDenied:
                _write_html(self, HTTPStatus.FORBIDDEN, ui1.render_blocked_html())
            except UI2AccessDenied:
                _write_html(self, HTTPStatus.FORBIDDEN, _blocked_html())
            except (
                UI2BoundaryError,
                ui1.UI1IntegrityError,
                ui1.UI1BoundaryError,
                p704.P704Error,
                OSError,
                ValueError,
            ):
                _write_html(self, HTTPStatus.SERVICE_UNAVAILABLE, _blocked_html())

        def do_GET(self) -> None:  # noqa: N802
            self._get()

        def do_HEAD(self) -> None:  # noqa: N802
            self._get()

        def do_POST(self) -> None:  # noqa: N802
            if urlsplit(self.path).path != "/interaction/execute":
                _write_html(self, HTTPStatus.METHOD_NOT_ALLOWED, _blocked_html())
                return
            try:
                _require_same_origin(self)
                fields = _read_form(self)
                if not hmac.compare_digest(fields["csrf"], csrf_token):
                    raise UI2BoundaryError("CSRF continuity mismatch")
                interaction_id = fields["interaction_id"].strip()
                snapshot = self._snapshot()
                self._interaction_access()
                case = _provider_case(interaction_provider, interaction_id)
                if case is None:
                    _write_html(self, HTTPStatus.NOT_FOUND, _blocked_html())
                    return

                # Security boundary: do not trust GET/form/button state.  The
                # governed preflight, source authorization freshness, optional
                # authorized reconstruction view and P7.04 technical access are
                # all re-evaluated in this POST before any governed action request.
                preflight_for_evidence = build_governed_interaction_preflight(
                    snapshot.workspace,
                    case=case,
                )
                reconstruction_html = ""
                if not isinstance(preflight_for_evidence, GovernedInteractionBlocked):
                    reconstruction_html = self._reconstruction_html(case, interaction_id)

                result = execute_governed_interaction(snapshot.workspace, case=case)
                outcome_evidence_html = ""
                if not isinstance(result.preflight, GovernedInteractionBlocked):
                    outcome_evidence_html = render_consequential_outcome_evidence_html(
                        inspect_consequential_outcome_evidence(
                            result.runtime_state,
                            execution_subject_id=(
                                case.execution_lineage.head().execution_subject_id
                            ),
                        )
                    )
                body = (
                    render_governed_interaction_preflight_html(result.preflight)
                    + reconstruction_html
                    + outcome_evidence_html
                    + render_governed_interaction_result_html(result)
                )
                _write_html(self, HTTPStatus.OK, _interaction_document(snapshot, body))
            except (UI2AccessDenied, UI2BoundaryError, ui1.UI1AccessDenied):
                _write_html(self, HTTPStatus.FORBIDDEN, _blocked_html())
            except (
                ui1.UI1IntegrityError,
                ui1.UI1BoundaryError,
                p704.P704Error,
                OSError,
                ValueError,
            ):
                _write_html(self, HTTPStatus.SERVICE_UNAVAILABLE, _blocked_html())

        def _reject_mutation(self) -> None:
            _write_html(self, HTTPStatus.METHOD_NOT_ALLOWED, _blocked_html())

        do_PUT = _reject_mutation
        do_PATCH = _reject_mutation
        do_DELETE = _reject_mutation

    return ThreadingHTTPServer((host, port), Handler)
