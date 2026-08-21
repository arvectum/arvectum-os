from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from .release import WorkspaceRelease

HASHED_ASSET = re.compile(r".+-[A-Za-z0-9_-]{6,}\.(?:js|css)$")


class AssetVerificationError(RuntimeError):
    pass


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        digest.update(_sha256_file(path).encode("ascii"))
    return digest.hexdigest()


def verify_frontend_assets(frontend_root: Path, release: WorkspaceRelease) -> dict[str, Any]:
    frontend_root = frontend_root.resolve()
    lock = frontend_root / "package-lock.json"
    dist = frontend_root / "dist"
    index = dist / "index.html"
    manifest = dist / ".vite" / "manifest.json"
    for path, label in ((lock, "package lock"), (index, "built index"), (manifest, "Vite manifest")):
        if not path.is_file():
            raise AssetVerificationError(f"{label} missing: {path}")
    html = index.read_text(encoding="utf-8")
    if "/src/" in html or "src/main.tsx" in html:
        raise AssetVerificationError("built index still references source modules")
    try:
        vite_manifest = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AssetVerificationError("Vite manifest unreadable") from exc
    if not isinstance(vite_manifest, dict) or not vite_manifest:
        raise AssetVerificationError("Vite manifest empty")
    assets_dir = dist / "assets"
    assets = [path.name for path in assets_dir.iterdir() if path.is_file()] if assets_dir.is_dir() else []
    if not any(HASHED_ASSET.fullmatch(name) for name in assets):
        raise AssetVerificationError("content-hashed frontend assets not found")
    source_bundle = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in sorted(assets_dir.iterdir())
        if path.is_file() and path.suffix == ".js"
    )
    if release.release_id not in source_bundle:
        raise AssetVerificationError("frontend bundle is not pinned to the declared application release")
    if "localStorage" in source_bundle or "sessionStorage" in source_bundle:
        raise AssetVerificationError("forbidden browser Web Storage reference found in production bundle")
    return {
        "status": "PASS",
        "release_id": release.release_id,
        "app_api_contract": release.app_api_contract,
        "frontend_dist_sha256": _tree_hash(dist),
        "package_lock_sha256": _sha256_file(lock),
        "content_hashed_assets": sorted(assets),
        "node_runtime_required": False,
    }


__all__ = ["AssetVerificationError", "verify_frontend_assets"]
