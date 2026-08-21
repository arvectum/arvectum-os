from __future__ import annotations

import ipaddress
import logging
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .access import AccessContext, AccessResolver, P704AccessResolver, WorkspaceAccessError
from .attention import AttentionProvider, RuntimeAttentionProvider
from .config import WorkspaceSettings
from .discovery import DiscoveryError, DiscoveryKind, DiscoveryProvider, ObjectUnavailable, RuntimeDiscoveryProvider
from .governed import GovernedExperienceError, GovernedExperienceProvider, RuntimeGovernedExperienceProvider
from .products import ProductSurfacesError, ProductSurfacesProvider, RuntimeProductSurfacesProvider
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
        {"id": "my-work", "label": "My Work", "href": "/my-work", "availability": "available"},
        {"id": "search", "label": "Search", "href": "/search", "availability": "available"},
        {"id": "records", "label": "Records", "href": "/records", "availability": "available"},
        {"id": "documents", "label": "Documents", "href": "/documents", "availability": "available"},
        {"id": "knowledge", "label": "Knowledge", "href": "/knowledge", "availability": "available"},
        {"id": "governed", "label": "Governed actions", "href": "/governed", "availability": "available"},
        {"id": "products", "label": "Products", "href": "/products", "availability": "available"},
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
    attention_provider: AttentionProvider | None = None,
    discovery_provider: DiscoveryProvider | None = None,
    governed_provider: GovernedExperienceProvider | None = None,
    product_surfaces_provider: ProductSurfacesProvider | None = None,
    session_store: SessionStore | None = None,
    static_dir: Path | None = None,
) -> FastAPI:
    settings = settings or WorkspaceSettings.from_env()
    release = load_release()
    resolver = access_resolver or P704AccessResolver(settings.runtime_root)
    attention = attention_provider or RuntimeAttentionProvider(settings.runtime_root)
    discovery = discovery_provider or RuntimeDiscoveryProvider(settings.runtime_root)
    governed = governed_provider or RuntimeGovernedExperienceProvider(settings.runtime_root)
    products = product_surfaces_provider or RuntimeProductSurfacesProvider(settings.runtime_root)
    store = session_store or SessionStore(
        idle_seconds=settings.session_idle_seconds,
        absolute_seconds=settings.session_absolute_seconds,
    )
    static_root = static_dir or (Path(__file__).resolve().parent.parent / "workspace_frontend" / "dist")

    app = FastAPI(title="Arvectum OS Productive Workspace BFF", docs_url=None, redoc_url=None, openapi_url=None)
    app.state.settings = settings
    app.state.release = release
    app.state.access_resolver = resolver
    app.state.attention_provider = attention
    app.state.discovery_provider = discovery
    app.state.governed_provider = governed
    app.state.product_surfaces_provider = products
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

    def _require_empty_governed_request(request: Request) -> None:
        if request.headers.get("transfer-encoding"):
            _security_event("GOVERNED_PREFLIGHT_INPUT_REJECTED", request, store, "transfer-encoding")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="GOVERNED_PREFLIGHT_INPUT_REJECTED")
        raw_length = request.headers.get("content-length")
        if raw_length is None:
            return
        try:
            length = int(raw_length)
        except ValueError:
            _security_event("GOVERNED_PREFLIGHT_INPUT_REJECTED", request, store, "invalid-content-length")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="GOVERNED_PREFLIGHT_INPUT_REJECTED") from None
        if length != 0:
            _security_event("GOVERNED_PREFLIGHT_INPUT_REJECTED", request, store, "non-empty-body")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="GOVERNED_PREFLIGHT_INPUT_REJECTED")

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

    @app.get("/api/app/v1/my-work")
    async def read_my_work(current: tuple[WorkspaceSession, AccessContext] = Depends(_authorize_current)) -> dict[str, Any]:
        _, access = current
        return attention.project(access).to_payload()

    @app.get("/api/app/v1/discovery")
    async def read_discovery(
        q: str = "",
        kind: str | None = None,
        current: tuple[WorkspaceSession, AccessContext] = Depends(_authorize_current),
    ) -> dict[str, Any]:
        _, access = current
        try:
            kind_filter = DiscoveryKind(kind) if kind is not None else None
            return discovery.search(access, query=q, kind=kind_filter).to_payload()
        except (ValueError, DiscoveryError):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="DISCOVERY_QUERY_INVALID") from None

    @app.get("/api/app/v1/objects/{object_id}")
    async def read_object_context(
        object_id: str,
        current: tuple[WorkspaceSession, AccessContext] = Depends(_authorize_current),
    ) -> dict[str, Any]:
        _, access = current
        try:
            return discovery.inspect(access, object_id).to_payload()
        except ObjectUnavailable:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OBJECT_UNAVAILABLE") from None
        except DiscoveryError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="DISCOVERY_UNAVAILABLE") from None

    @app.get("/api/app/v1/governed")
    async def read_governed_experience(
        current: tuple[WorkspaceSession, AccessContext] = Depends(_authorize_current),
    ) -> dict[str, object]:
        _, access = current
        try:
            return governed.inspect(access).to_payload()
        except GovernedExperienceError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="GOVERNED_EXPERIENCE_UNAVAILABLE") from None

    @app.get("/api/app/v1/products")
    async def read_product_surfaces(
        current: tuple[WorkspaceSession, AccessContext] = Depends(_authorize_current),
    ) -> dict[str, object]:
        _, access = current
        try:
            return products.project(access).to_payload()
        except ProductSurfacesError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="PRODUCT_SURFACES_UNAVAILABLE") from None

    @app.post("/api/app/v1/governed/preflight")
    async def run_governed_preflight(
        request: Request,
        current: tuple[WorkspaceSession, AccessContext] = Depends(_csrf_protected),
    ) -> dict[str, object]:
        _require_empty_governed_request(request)
        _, access = current
        try:
            return governed.run_preflight(access).to_payload()
        except GovernedExperienceError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="GOVERNED_PREFLIGHT_UNAVAILABLE") from None

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