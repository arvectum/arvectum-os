from __future__ import annotations

import ipaddress
import logging
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .access import AccessContext, AccessResolver, P704AccessResolver, WorkspaceAccessError
from .config import WorkspaceSettings
from .release import WorkspaceRelease, load_release
from .security import SessionStore, WorkspaceSession

logger = logging.getLogger("arvectum.workspace.security")
SAFE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})
RELEASE_HEADER = "X-Arvectum-Workspace-Release"
CSRF_HEADER = "X-Arvectum-CSRF"


def _is_loopback_client(host: str | None) -> bool:
    if not host:
        return False
    normalized = host.strip("[]").lower()
    if normalized == "localhost":
        return True
    try:
        return ipaddress.ip_address(normalized).is_loopback
    except ValueError:
        return False


def _identity_key(identity: object) -> tuple[str, str, str]:
    return (identity.namespace, identity.value, identity.scope)  # type: ignore[attr-defined]


def _security_event(code: str, request: Request, store: SessionStore, detail: str = "") -> None:
    session_id = request.cookies.get(request.app.state.settings.cookie_name)
    logger.warning(
        "workspace_security_event code=%s method=%s path=%s session=%s detail=%s",
        code,
        request.method,
        request.url.path,
        store.correlation_id(session_id),
        detail[:160],
    )


def _navigation() -> list[dict[str, Any]]:
    return [
        {"id": "home", "label": "Home", "href": "/", "availability": "available"},
        {"id": "my-work", "label": "My Work", "href": "/my-work", "availability": "planned-p9.04"},
        {"id": "search", "label": "Search", "href": "/search", "availability": "planned-p9.05"},
        {"id": "governed", "label": "Governed actions", "href": "/governed", "availability": "planned-p9.06"},
        {"id": "products", "label": "Products", "href": "/products", "availability": "planned-p9.07"},
    ]


def _context_payload(*, settings: WorkspaceSettings, release: WorkspaceRelease, session: WorkspaceSession) -> dict[str, Any]:
    return {
        "schema": "arvectum.workspace.shell-context/1",
        "release": {
            "id": release.release_id,
            "app_api_contract": release.app_api_contract,
            "classification": release.classification,
            "public_api": release.public_api,
        },
        "organization": {"label": settings.organization_label, "scope_resolved_server_side": True},
        "actor": {
            "label": settings.actor_label,
            "attributable": True,
            "scope_resolved_server_side": True,
            "authentication_source": session.authentication_source,
        },
        "session": {
            "csrf_token": session.csrf_token,
            "bounded": True,
            "revocable": True,
            "authority_provided": False,
        },
        "navigation": _navigation(),
        "data_governance": {
            "protected_read_revalidated": True,
            "response_minimized": "shell-context-only",
            "canonical_state_in_browser": False,
        },
    }


def create_app(
    settings: WorkspaceSettings | None = None,
    *,
    access_resolver: AccessResolver | None = None,
    session_store: SessionStore | None = None,
    static_dir: Path | None = None,
) -> FastAPI:
    settings = settings or WorkspaceSettings.from_env()
    release = load_release()
    resolver = access_resolver or P704AccessResolver(settings.runtime_root)
    store = session_store or SessionStore(
        idle_seconds=settings.session_idle_seconds,
        absolute_seconds=settings.session_absolute_seconds,
    )
    static_root = static_dir or (Path(__file__).resolve().parent.parent / "workspace_frontend" / "dist")

    app = FastAPI(title="Arvectum OS Productive Workspace BFF", docs_url=None, redoc_url=None, openapi_url=None)
    app.state.settings = settings
    app.state.release = release
    app.state.access_resolver = resolver
    app.state.session_store = store
    app.state.static_root = static_root

    @app.middleware("http")
    async def trust_boundary(request: Request, call_next):  # type: ignore[no-untyped-def]
        host = request.headers.get("host", "").lower()
        if host not in settings.allowed_hosts:
            _security_event("HOST_REJECTED", request, store, host)
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"code": "HOST_REJECTED"})

        if request.method not in SAFE_METHODS:
            origin = request.headers.get("origin")
            if origin != settings.public_origin:
                _security_event("ORIGIN_REJECTED", request, store, origin or "missing")
                return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"code": "ORIGIN_REJECTED"})

        if request.url.path.startswith("/api/app/v1"):
            supplied_release = request.headers.get(RELEASE_HEADER)
            if supplied_release != release.release_id:
                _security_event("RELEASE_MISMATCH", request, store, supplied_release or "missing")
                return JSONResponse(
                    status_code=status.HTTP_409_CONFLICT,
                    content={"code": "RELEASE_MISMATCH", "reload_required": True},
                    headers={RELEASE_HEADER: release.release_id, "Cache-Control": "no-store"},
                )

        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
            "connect-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
        )
        if request.url.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store"
            response.headers[RELEASE_HEADER] = release.release_id
        elif request.url.path.startswith("/assets/"):
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        else:
            response.headers["Cache-Control"] = "no-store"
        return response

    def _authorize_current(request: Request) -> tuple[WorkspaceSession, AccessContext]:
        session_id = request.cookies.get(settings.cookie_name)
        session = store.get(session_id)
        if session is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="SESSION_REQUIRED")
        try:
            access = resolver.authorize()
        except WorkspaceAccessError as exc:
            store.revoke(session_id)
            _security_event("ACCESS_REVALIDATION_DENIED", request, store, str(exc))
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ACCESS_DENIED") from exc
        if session.organization_key != _identity_key(access.organization) or session.actor_key != _identity_key(access.actor):
            store.revoke(session_id)
            _security_event("CONTEXT_BINDING_CHANGED", request, store)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CONTEXT_CHANGED")
        return session, access

    def _csrf_protected(
        request: Request,
        current: tuple[WorkspaceSession, AccessContext] = Depends(_authorize_current),
    ) -> tuple[WorkspaceSession, AccessContext]:
        session, access = current
        if not store.csrf_matches(session, request.headers.get(CSRF_HEADER)):
            _security_event("CSRF_REJECTED", request, store)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CSRF_REJECTED")
        return session, access

    @app.post("/api/app/v1/session/bootstrap")
    async def bootstrap_session(request: Request, response: Response) -> dict[str, Any]:
        if not _is_loopback_client(request.client.host if request.client else None):
            _security_event("BOOTSTRAP_NON_LOOPBACK", request, store)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="LOOPBACK_REQUIRED")
        if not settings.allow_loopback_http and not settings.secure_cookie:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="SECURITY_PROFILE_UNAVAILABLE")
        try:
            access = resolver.authorize()
        except WorkspaceAccessError as exc:
            _security_event("BOOTSTRAP_ACCESS_DENIED", request, store, str(exc))
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ACCESS_DENIED") from exc
        session = store.rotate(request.cookies.get(settings.cookie_name), access)
        response.set_cookie(
            key=settings.cookie_name,
            value=session.session_id,
            max_age=settings.session_absolute_seconds,
            httponly=True,
            secure=settings.secure_cookie,
            samesite="strict",
            path="/",
        )
        return _context_payload(settings=settings, release=release, session=session)

    @app.get("/api/app/v1/context")
    async def read_context(current: tuple[WorkspaceSession, AccessContext] = Depends(_authorize_current)) -> dict[str, Any]:
        session, _ = current
        return _context_payload(settings=settings, release=release, session=session)

    @app.post("/api/app/v1/session/logout")
    async def logout(
        request: Request,
        response: Response,
        current: tuple[WorkspaceSession, AccessContext] = Depends(_csrf_protected),
    ) -> dict[str, str]:
        session, _ = current
        store.revoke(session.session_id)
        response.delete_cookie(
            settings.cookie_name,
            path="/",
            secure=settings.secure_cookie,
            httponly=True,
            samesite="strict",
        )
        return {"status": "logged_out"}

    if static_root.is_dir():
        assets = static_root / "assets"
        if assets.is_dir():
            app.mount("/assets", StaticFiles(directory=assets), name="workspace-assets")

    @app.get("/{path:path}")
    async def spa(path: str) -> Response:
        if path.startswith("api/") or path.startswith("assets/"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        index = static_root / "index.html"
        if not index.is_file():
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"code": "WORKSPACE_ASSETS_UNAVAILABLE"},
            )
        return FileResponse(index, media_type="text/html")

    return app
