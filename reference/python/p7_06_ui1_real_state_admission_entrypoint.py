#!/usr/bin/env python3
"""Hardened selected-Mac entrypoint for the bounded P7.06-UI1 real-state admission.

The implementation module performs the Governed Execution/admission/persistence
flow. This entrypoint adds a fail-closed semantic check for an already-retained
exact Subject/Version before allowing the implementation's idempotent retry path.
It is the required owner-operated entrypoint for the selected-Mac proof.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Mapping

from arvectum_os_ref.canonical import AuthorityMode
import p7_03_durable_state as p703
import p7_06_ui1_real_state_admission as admission

EXPECTED_VALIDATION_STATUS = (
    "CAP-001 admitted; RFC-0006 provenance admitted; CAP-004 reconstruction complete"
)


class UI1RealStateEntrypointError(RuntimeError):
    """Fail-closed semantic continuity error for selected-Mac retry."""


def _matching_exact_items(
    runtime_root: Path,
    *,
    subject_identity: str,
    version_identity: str,
) -> tuple[tuple[str, Mapping[str, Any]], ...]:
    p703.verify_store(runtime_root)
    items_root = runtime_root.expanduser().resolve() / "state" / "governed" / "items"
    matches: list[tuple[str, Mapping[str, Any]]] = []
    for child in sorted(items_root.iterdir()):
        manifest = p703.verify_item(child)
        metadata = manifest.get("metadata", {})
        if metadata.get("state_class") != "canonical-governed-state":
            continue
        if (
            metadata.get("subject_identity") == subject_identity
            and metadata.get("version_identity") == version_identity
        ):
            matches.append((child.name, metadata))
    return tuple(matches)


def verify_existing_retry_semantics(
    runtime_root: Path,
    *,
    subject_identity: str,
    version_identity: str,
) -> str | None:
    """Return the existing exact item id only if full admitted semantics match."""
    matches = _matching_exact_items(
        runtime_root,
        subject_identity=subject_identity,
        version_identity=version_identity,
    )
    if len(matches) > 1:
        raise UI1RealStateEntrypointError(
            "multiple canonical-governed-state items claim the exact Subject/Version"
        )
    if not matches:
        return None

    item_id, metadata = matches[0]
    required_exact = {
        "state_class": "canonical-governed-state",
        "semantic_type": "platform.document",
        "schema_version": "p7.06-ui1-real-eis-evidence-1",
        "classification": admission.PERSISTED_CLASSIFICATION,
        "retention_policy_ref": admission.PERSISTED_RETENTION,
        "subject_identity": subject_identity,
        "version_identity": version_identity,
        "authority_mode": AuthorityMode.EXTERNAL_REFERENCE.value,
        "authority_scope": admission.DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
        "authoritative_source": admission.EXTERNAL_SOURCE_AUTHORITY,
        "validation_status": EXPECTED_VALIDATION_STATUS,
        "source_manifest_sha256": admission.APPROVED_MANIFEST_SHA256,
        "product_contract_version": "0.1.0",
        "canonical_authority": True,
        "contains_reusable_secret": False,
        "raw_document_bytes_included": False,
        "external_actions": False,
    }
    for key, expected in required_exact.items():
        if metadata.get(key) != expected:
            raise UI1RealStateEntrypointError(
                f"existing exact Subject/Version has incompatible retained metadata: {key}"
            )

    admission_ref = metadata.get("governed_admission_ref")
    provenance_refs = metadata.get("provenance_refs")
    source_release_sha = metadata.get("source_release_sha")
    if not isinstance(admission_ref, str) or not admission_ref.strip():
        raise UI1RealStateEntrypointError("existing exact item lacks governed admission reference")
    if not isinstance(provenance_refs, list) or len(provenance_refs) < 5:
        raise UI1RealStateEntrypointError("existing exact item lacks bounded provenance chain")
    if any(not isinstance(value, str) or not value.strip() for value in provenance_refs):
        raise UI1RealStateEntrypointError("existing exact item has malformed provenance references")
    if not isinstance(source_release_sha, str) or len(source_release_sha) != 40:
        raise UI1RealStateEntrypointError("existing exact item lacks exact source release SHA")
    return item_id


def run_selected_mac_admission(**kwargs):
    """Run hardened selected-Mac admission with strict pre-existing state semantics."""
    if kwargs.get("owner_approval") != admission.OWNER_APPROVAL_ASSERTION:
        raise UI1RealStateEntrypointError("exact bounded owner approval assertion is required")

    runtime_root = Path(kwargs["runtime_root"])
    release_sha, repo_root = admission._verify_exact_release(runtime_root)
    organization, principal, _decision = admission._authorize_operator(
        access_root=Path(kwargs["access_root"]),
        state_file=Path(kwargs["state_file"]),
        credential_id=str(kwargs["credential_id"]),
        credential_file=Path(kwargs["credential_file"]),
    )
    rc, _lines, connection = admission.connect_product(
        Path(kwargs["state_file"]),
        arvectum_repo_root=repo_root,
    )
    if rc != 0 or connection is None:
        raise UI1RealStateEntrypointError("P6.02 Product Contract connection/preflight failed")
    if connection.organization_scope.organization_id != organization:
        raise UI1RealStateEntrypointError("P6.05-L4 Organization continuity mismatch")
    if connection.principal.principal_id != principal:
        raise UI1RealStateEntrypointError("P6.05-L4 human Principal continuity mismatch")

    subject_identity, version_identity = admission._target_identity_pair(connection)
    verify_existing_retry_semantics(
        runtime_root,
        subject_identity=subject_identity,
        version_identity=version_identity,
    )

    result = admission.run_admission(**kwargs)
    if result.release_sha != release_sha:
        raise UI1RealStateEntrypointError("admission result release drifted from exact preflight release")
    return result


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-root", type=Path, required=True)
    parser.add_argument("--access-root", type=Path, required=True)
    parser.add_argument("--state-file", type=Path, required=True)
    parser.add_argument("--credential-id", required=True)
    parser.add_argument("--credential-file", type=Path, required=True)
    parser.add_argument("--l7-manifest", type=Path, required=True)
    parser.add_argument("--owner-approval", required=True)
    parser.add_argument("--evidence-output", type=Path)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        result = run_selected_mac_admission(
            runtime_root=args.runtime_root,
            access_root=args.access_root,
            state_file=args.state_file,
            credential_id=args.credential_id,
            credential_file=args.credential_file,
            l7_manifest=args.l7_manifest,
            owner_approval=args.owner_approval,
            evidence_output=args.evidence_output,
        )
    except Exception as exc:
        print(f"RESULT=BLOCKED error={type(exc).__name__}:{exc}")
        return 2

    print(f"RESULT={result.status}")
    print(f"RELEASE_SHA={result.release_sha}")
    print(f"STORAGE_ITEM_ID={result.storage_item_id}")
    print(f"CHECKPOINT_ID={result.checkpoint_id or 'NONE'}")
    print(f"MANIFEST_SHA256={result.manifest_sha256}")
    print(f"IDEMPOTENT_EXISTING_ITEM={str(result.idempotent_existing_item).lower()}")
    print(f"RECONSTRUCTION_COMPLETE={str(result.reconstruction_complete).lower()}")
    print(f"EVIDENCE_PATH={result.evidence_path}")
    print("NETWORK_INVOKED=false")
    print("EXTERNAL_ACTIONS=false")
    print("RAW_DOCUMENT_BYTES_PERSISTED=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
