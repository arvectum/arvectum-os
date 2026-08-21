from __future__ import annotations

import hashlib
import hmac
import secrets
import threading
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Callable

from .access import AccessContext


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class WorkspaceSession:
    session_id: str
    organization_key: tuple[str, str, str]
    actor_key: tuple[str, str, str]
    authentication_source: str
    csrf_token: str
    created_at: datetime
    last_activity_at: datetime
    idle_expires_at: datetime
    absolute_expires_at: datetime
    revoked: bool = False


class SessionStore:
    """Bounded in-memory server-side session state for the P9.03 contour.

    Process restart invalidates all sessions fail-closed. No canonical state or
    Organizational Authority is stored here.
    """

    def __init__(
        self,
        *,
        idle_seconds: int,
        absolute_seconds: int,
        clock: Callable[[], datetime] = _utcnow,
    ) -> None:
        self.idle_seconds = idle_seconds
        self.absolute_seconds = absolute_seconds
        self._clock = clock
        self._sessions: dict[str, WorkspaceSession] = {}
        self._lock = threading.RLock()
        self._correlation_salt = secrets.token_bytes(32)

    @staticmethod
    def _key(identity: object) -> tuple[str, str, str]:
        return (identity.namespace, identity.value, identity.scope)  # type: ignore[attr-defined]

    def create(self, access: AccessContext) -> WorkspaceSession:
        now = self._clock()
        session = WorkspaceSession(
            session_id=secrets.token_urlsafe(48),
            organization_key=self._key(access.organization),
            actor_key=self._key(access.actor),
            authentication_source=access.authentication_source,
            csrf_token=secrets.token_urlsafe(32),
            created_at=now,
            last_activity_at=now,
            idle_expires_at=now + timedelta(seconds=self.idle_seconds),
            absolute_expires_at=now + timedelta(seconds=self.absolute_seconds),
        )
        with self._lock:
            self._sessions[session.session_id] = session
        return session

    def get(self, session_id: str | None, *, touch: bool = True) -> WorkspaceSession | None:
        if not session_id:
            return None
        now = self._clock()
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None or session.revoked:
                return None
            if now >= session.idle_expires_at or now >= session.absolute_expires_at:
                session.revoked = True
                self._sessions.pop(session_id, None)
                return None
            if touch:
                session.last_activity_at = now
                session.idle_expires_at = min(
                    now + timedelta(seconds=self.idle_seconds),
                    session.absolute_expires_at,
                )
            return session

    def revoke(self, session_id: str | None) -> None:
        if not session_id:
            return
        with self._lock:
            session = self._sessions.pop(session_id, None)
            if session is not None:
                session.revoked = True

    def rotate(self, session_id: str | None, access: AccessContext) -> WorkspaceSession:
        self.revoke(session_id)
        return self.create(access)

    def correlation_id(self, session_id: str | None) -> str:
        if not session_id:
            return "none"
        digest = hashlib.sha256(self._correlation_salt + session_id.encode("utf-8")).hexdigest()
        return digest[:16]

    @staticmethod
    def csrf_matches(session: WorkspaceSession, supplied: str | None) -> bool:
        return bool(supplied) and hmac.compare_digest(session.csrf_token, supplied)


__all__ = ["SessionStore", "WorkspaceSession"]
