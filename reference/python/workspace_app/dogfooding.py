from __future__ import annotations

import hashlib
import json
import os
import threading
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .access import AccessContext


DOGFOODING_SCHEMA = "arvectum.workspace.dogfooding-backlog/1"
OBSERVATION_SCHEMA = "arvectum.workspace.dogfooding-observation/1"
MAX_ITEMS = 200
RETENTION_DAYS = 90

JOURNEYS = frozenset({"J1", "J2", "J3", "J4", "J5", "J6", "other"})
SURFACES = frozenset(
    {
        "home",
        "organization",
        "my-work",
        "activity",
        "search",
        "records-documents-knowledge",
        "ask-arvectum",
        "governed-actions",
        "products",
        "other",
    }
)
SEVERITIES = frozenset({"blocker", "material", "minor"})
CLASSIFICATIONS = frozenset({"workspace-usability", "product-specific", "governance", "security-authority"})
DISPOSITIONS = frozenset({"resolved", "routed-product", "routed-governance", "not-reproducible", "deferred"})


class DogfoodingError(RuntimeError):
    pass


class DogfoodingInputError(DogfoodingError):
    pass


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _scope_key(identity: object) -> str:
    material = "\0".join(
        (
            str(getattr(identity, "namespace")),
            str(getattr(identity, "value")),
            str(getattr(identity, "scope")),
        )
    ).encode("utf-8")
    return hashlib.sha256(material).hexdigest()[:24]


def _bounded_text(value: object, *, field: str, maximum: int, required: bool = True) -> str:
    if not isinstance(value, str):
        raise DogfoodingInputError(f"{field} must be text")
    normalized = " ".join(value.split())
    if required and not normalized:
        raise DogfoodingInputError(f"{field} is required")
    if len(normalized) > maximum:
        raise DogfoodingInputError(f"{field} exceeds {maximum} characters")
    return normalized


def normalize_observation(payload: object) -> dict[str, str]:
    if not isinstance(payload, dict):
        raise DogfoodingInputError("observation payload must be an object")
    required = {"journey", "surface", "severity", "classification", "summary", "details"}
    if set(payload) != required:
        raise DogfoodingInputError("observation payload has unexpected fields")

    result = {
        "journey": _bounded_text(payload["journey"], field="journey", maximum=12),
        "surface": _bounded_text(payload["surface"], field="surface", maximum=48),
        "severity": _bounded_text(payload["severity"], field="severity", maximum=16),
        "classification": _bounded_text(payload["classification"], field="classification", maximum=32),
        "summary": _bounded_text(payload["summary"], field="summary", maximum=240),
        "details": _bounded_text(payload["details"], field="details", maximum=600, required=False),
    }
    if result["journey"] not in JOURNEYS:
        raise DogfoodingInputError("unsupported journey")
    if result["surface"] not in SURFACES:
        raise DogfoodingInputError("unsupported surface")
    if result["severity"] not in SEVERITIES:
        raise DogfoodingInputError("unsupported severity")
    if result["classification"] not in CLASSIFICATIONS:
        raise DogfoodingInputError("unsupported classification")
    return result


def normalize_disposition(payload: object) -> dict[str, str]:
    if not isinstance(payload, dict) or set(payload) != {"disposition", "rationale"}:
        raise DogfoodingInputError("disposition payload has unexpected fields")
    disposition = _bounded_text(payload["disposition"], field="disposition", maximum=32)
    rationale = _bounded_text(payload["rationale"], field="rationale", maximum=500)
    if disposition not in DISPOSITIONS:
        raise DogfoodingInputError("unsupported disposition")
    return {"disposition": disposition, "rationale": rationale}


def _validate_disposition(item: dict[str, Any], disposition: str) -> None:
    classification = item.get("classification")
    severity = item.get("severity")
    if severity == "blocker" and disposition not in {"resolved", "not-reproducible"}:
        raise DogfoodingInputError("blockers must remain open until resolved or shown not reproducible")
    if disposition == "routed-product" and classification != "product-specific":
        raise DogfoodingInputError("only product-specific observations can route to product backlog")
    if disposition == "routed-governance" and classification not in {"governance", "security-authority"}:
        raise DogfoodingInputError("only governance or security-authority observations can route to governance")
    if classification == "security-authority" and disposition in {"deferred", "routed-product"}:
        raise DogfoodingInputError("security-authority observations cannot be deferred or routed to product backlog")


@dataclass(frozen=True)
class DogfoodingProjection:
    generated_at: str
    items: tuple[dict[str, Any], ...]

    def to_payload(self) -> dict[str, Any]:
        open_items = sum(1 for item in self.items if item["status"] == "open")
        material_open = sum(
            1
            for item in self.items
            if item["status"] == "open" and item["severity"] in {"blocker", "material"}
        )
        closure_blocking = sum(
            1
            for item in self.items
            if item["severity"] in {"blocker", "material"}
            and (item["status"] == "open" or item.get("disposition") == "deferred")
        )
        return {
            "schema": DOGFOODING_SCHEMA,
            "generated_at": self.generated_at,
            "projection": {
                "derived": True,
                "canonical_authority": False,
                "canonical_event": False,
                "validated_knowledge": False,
                "organizational_authority_provided": False,
                "consequential_action_available": False,
            },
            "scope": {
                "organization_resolved_server_side": True,
                "actor_resolved_server_side": True,
                "current_access_revalidated": True,
                "cross_organization_aggregation": False,
            },
            "retention": {
                "bounded": True,
                "days": RETENTION_DAYS,
                "max_items": MAX_ITEMS,
                "free_text_minimized": True,
                "pruned_on_access": True,
            },
            "summary": {
                "total": len(self.items),
                "open": open_items,
                "material_open": material_open,
                "closure_blocking": closure_blocking,
            },
            "items": list(self.items),
        }


class DogfoodingStore:
    """Owner-operated, non-canonical P9.11 observation store.

    This is intentionally not an RFC-0006 Event store and not RFC-0007 Knowledge.
    It keeps bounded local usability observations until canonical P9.11 review evidence
    dispositions the backlog.
    """

    def __init__(self, runtime_root: Path) -> None:
        self.path = runtime_root / "workspace" / "p9-11" / "friction-observations.json"
        self._lock = threading.Lock()

    def _read_all(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise DogfoodingError("dogfooding observation store is unavailable") from exc
        if not isinstance(raw, list) or any(not isinstance(item, dict) for item in raw):
            raise DogfoodingError("dogfooding observation store is invalid")
        return raw

    def _write_all(self, items: list[dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(self.path.parent, 0o700)
        except OSError:
            pass
        temporary = self.path.with_suffix(".tmp")
        try:
            temporary.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            try:
                os.chmod(temporary, 0o600)
            except OSError:
                pass
            os.replace(temporary, self.path)
        except OSError as exc:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass
            raise DogfoodingError("dogfooding observation store could not be persisted") from exc

    @staticmethod
    def _retained(items: list[dict[str, Any]], now: datetime) -> list[dict[str, Any]]:
        cutoff = now - timedelta(days=RETENTION_DAYS)
        retained: list[dict[str, Any]] = []
        for item in items:
            recorded_at = item.get("recorded_at")
            if not isinstance(recorded_at, str):
                raise DogfoodingError("dogfooding observation has no valid recording time")
            try:
                parsed = datetime.fromisoformat(recorded_at.replace("Z", "+00:00"))
            except ValueError as exc:
                raise DogfoodingError("dogfooding observation has invalid recording time") from exc
            if parsed.tzinfo is None:
                raise DogfoodingError("dogfooding observation recording time is not timezone-aware")
            if parsed >= cutoff:
                retained.append(item)
        return retained[-MAX_ITEMS:]

    def _load_retained(self, now: datetime) -> list[dict[str, Any]]:
        raw = self._read_all()
        retained = self._retained(raw, now)
        if retained != raw:
            self._write_all(retained)
        return retained

    def project(self, access: AccessContext) -> DogfoodingProjection:
        organization_key = _scope_key(access.organization)
        now = _now()
        with self._lock:
            items = self._load_retained(now)
        visible = tuple(
            {key: value for key, value in item.items() if key not in {"organization_scope_key", "actor_scope_key"}}
            for item in items
            if item.get("organization_scope_key") == organization_key
        )
        return DogfoodingProjection(generated_at=_iso(now), items=visible)

    def record(self, access: AccessContext, release_id: str, payload: object) -> dict[str, Any]:
        normalized = normalize_observation(payload)
        now = _now()
        item: dict[str, Any] = {
            "schema": OBSERVATION_SCHEMA,
            "id": uuid.uuid4().hex,
            "recorded_at": _iso(now),
            "release_id": release_id,
            "organization_scope_key": _scope_key(access.organization),
            "actor_scope_key": _scope_key(access.actor),
            **normalized,
            "status": "open",
            "disposition": None,
            "disposition_rationale": None,
            "dispositioned_at": None,
        }
        with self._lock:
            items = self._load_retained(now)
            items.append(item)
            self._write_all(items[-MAX_ITEMS:])
        return {key: value for key, value in item.items() if key not in {"organization_scope_key", "actor_scope_key"}}

    def disposition(self, access: AccessContext, observation_id: str, payload: object) -> dict[str, Any]:
        normalized = normalize_disposition(payload)
        if not observation_id or len(observation_id) > 64:
            raise DogfoodingInputError("invalid observation id")
        organization_key = _scope_key(access.organization)
        now = _now()
        with self._lock:
            items = self._load_retained(now)
            matched: dict[str, Any] | None = None
            for item in items:
                if item.get("id") != observation_id or item.get("organization_scope_key") != organization_key:
                    continue
                if item.get("status") != "open":
                    raise DogfoodingInputError("observation is already dispositioned")
                _validate_disposition(item, normalized["disposition"])
                item["status"] = "dispositioned"
                item["disposition"] = normalized["disposition"]
                item["disposition_rationale"] = normalized["rationale"]
                item["dispositioned_at"] = _iso(now)
                matched = item
                break
            if matched is None:
                raise DogfoodingInputError("observation is unavailable")
            self._write_all(items)
        return {key: value for key, value in matched.items() if key not in {"organization_scope_key", "actor_scope_key"}}


__all__ = [
    "CLASSIFICATIONS",
    "DISPOSITIONS",
    "DOGFOODING_SCHEMA",
    "DogfoodingError",
    "DogfoodingInputError",
    "DogfoodingProjection",
    "DogfoodingStore",
    "JOURNEYS",
    "SEVERITIES",
    "SURFACES",
    "normalize_disposition",
    "normalize_observation",
]
