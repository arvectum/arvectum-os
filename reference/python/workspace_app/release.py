from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


class ReleaseMetadataError(RuntimeError):
    pass


@dataclass(frozen=True)
class WorkspaceRelease:
    release_id: str
    app_api_contract: str
    classification: str
    public_api: bool


@lru_cache(maxsize=1)
def load_release() -> WorkspaceRelease:
    path = Path(__file__).with_name("release.json")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReleaseMetadataError("Workspace release metadata is unreadable") from exc
    if set(payload) != {"schema", "release_id", "app_api_contract", "classification", "public_api"}:
        raise ReleaseMetadataError("Workspace release metadata shape is invalid")
    if payload["schema"] != "arvectum.workspace.application-release/1":
        raise ReleaseMetadataError("Workspace release metadata schema is unsupported")
    release_id = payload["release_id"]
    contract = payload["app_api_contract"]
    if not isinstance(release_id, str) or not release_id.strip() or not isinstance(contract, str) or not contract.strip():
        raise ReleaseMetadataError("Workspace release identity/contract must be non-empty")
    if payload["classification"] != "bounded-internal-provisional" or payload["public_api"] is not False:
        raise ReleaseMetadataError("Workspace release metadata overstates the P9.03 boundary")
    return WorkspaceRelease(
        release_id=release_id,
        app_api_contract=contract,
        classification=payload["classification"],
        public_api=False,
    )


__all__ = ["ReleaseMetadataError", "WorkspaceRelease", "load_release"]
