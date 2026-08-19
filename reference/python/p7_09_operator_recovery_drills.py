#!/usr/bin/env python3
"""P7.09 operator incident / uncertain-outcome / recovery drill evaluator.

This module is intentionally side-effect-free with respect to Arvectum OS canonical
state, product state, credentials, network services and external effects. It turns
strict operator-supplied observations into a deterministic recovery decision and can
record owner-local non-canonical drill receipts with SHA-256 sidecars.

It does not execute recovery automatically. The versioned runbook owns the exact
technical recovery commands. In particular, no result from this module grants
Organizational Authority, consequential approval or permission to replay a historical
external effect.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Optional

RUNBOOK_VERSION = "1.0.0"
DECISION_SCHEMA = "arvectum.p7_09.recovery-decision/1"
RECEIPT_SCHEMA = "arvectum.p7_09.drill-receipt/1"
OPERATING_MODE = "Persistent Internal / owner-operated"
ORGANIZATION_SCOPE = "ООО «Арвектум»"
SHA40_RE = re.compile(r"^[0-9a-f]{40}$")

PASS = "PASS"
FAIL_CLOSED = "FAIL_CLOSED"
RECONCILIATION_REQUIRED = "RECONCILIATION_REQUIRED"
FORWARD_RECOVERY_REQUIRED = "FORWARD_RECOVERY_REQUIRED"

SCENARIOS = (
    "runtime-crash",
    "mac-restart",
    "persistent-state-or-backup-unavailable",
    "network-proxy-tls-failure",
    "product-host-unavailable",
    "uncertain-external-effect",
    "partial-evidence-path",
    "credential-revocation-rotation",
    "failed-update-rollback",
)

COMMON_FIELDS: dict[str, Any] = {
    "operator_attributable": bool,
    "organization_scope_verified": bool,
    "reusable_secret_exposed": bool,
    "canonical_mutation_by_drill": bool,
    "external_effect_invoked_by_drill": bool,
}

SCENARIO_FIELDS: dict[str, dict[str, Any]] = {
    "runtime-crash": {
        "runtime_status_after": {"healthy", "degraded", "down"},
        "exact_release_verified": bool,
        "supervised_generation_advanced": bool,
        "historical_effect_replayed": bool,
    },
    "mac-restart": {
        "runtime_status_after": {"healthy", "degraded", "down"},
        "observer_loaded": bool,
        "exact_release_consistent": bool,
        "durable_state_integrity_verified": bool,
        "historical_effect_replayed": bool,
    },
    "persistent-state-or-backup-unavailable": {
        "live_state_available": bool,
        "live_state_integrity_verified": bool,
        "verified_backup_available": bool,
        "isolated_restore_verified": bool,
        "live_state_overwritten": bool,
    },
    "network-proxy-tls-failure": {
        "connectivity_restored": bool,
        "tls_trust_verified": bool,
        "external_effect_state": {"none", "confirmed-succeeded", "confirmed-not-executed", "unknown"},
        "historical_effect_replayed": bool,
    },
    "product-host-unavailable": {
        "product_host_reachable": bool,
        "product_contract_boundary_available": bool,
        "external_effect_state": {"none", "confirmed-succeeded", "confirmed-not-executed", "unknown"},
        "platform_bypass_used": bool,
    },
    "uncertain-external-effect": {
        "external_outcome": {"confirmed-succeeded", "confirmed-not-executed", "unknown"},
        "reconciliation_evidence_verified": bool,
        "historical_effect_replayed": bool,
        "new_effect_authorized": bool,
    },
    "partial-evidence-path": {
        "required_evidence_complete": bool,
        "integrity_verified": bool,
        "authoritative_source_known": bool,
        "fabricated_replacement_evidence": bool,
    },
    "credential-revocation-rotation": {
        "old_credential_denied": bool,
        "replacement_credential_verified": bool,
        "exact_grant_scope_verified": bool,
        "organizational_authority_inferred_from_access": bool,
        "reusable_secret_in_evidence": bool,
    },
    "failed-update-rollback": {
        "active_release_known": bool,
        "latest_transaction_known": bool,
        "state_schema_changed": bool,
        "rollback_safe": bool,
        "rollback_completed": bool,
        "runtime_healthy_after": bool,
        "observer_release_consistent": bool,
        "historical_effect_replayed": bool,
    },
}

RUNBOOK_ROUTES: dict[str, tuple[str, ...]] = {
    "runtime-crash": (
        "P7.02 status/crash-proof/restart",
        "P7.05 status",
    ),
    "mac-restart": (
        "P7.02 status",
        "P7.05 status",
        "P7.03 verify",
    ),
    "persistent-state-or-backup-unavailable": (
        "P7.03 verify",
        "P7.03 verify-backup",
        "P7.03 restore --target-root <new-isolated-target>",
    ),
    "network-proxy-tls-failure": (
        "P7.05 status",
        "external dependency/proxy/TLS diagnostics",
        "return to governed workflow only after dependency verification",
    ),
    "product-host-unavailable": (
        "preserve Product Contract boundary",
        "restore product host independently",
        "do not replace product authority with platform internals",
    ),
    "uncertain-external-effect": (
        "preserve uncertain/reconciliation-required state",
        "reconcile against authoritative external/product evidence",
        "P7.08 reconstruction only after confirmed outcome",
    ),
    "partial-evidence-path": (
        "stop consequential processing",
        "verify retained/canonical evidence and digests",
        "do not fabricate missing evidence",
    ),
    "credential-revocation-rotation": (
        "P7.04 revoke/rotate exact credential",
        "verify old credential denied",
        "verify replacement only on exact existing grant",
    ),
    "failed-update-rollback": (
        "P7.06 status",
        "P7.06 rollback-last when rollback-safe",
        "P7.06 recover-interrupted-latest when bounded interrupted evidence exists",
    ),
}


class P709Error(RuntimeError):
    pass


class BoundaryError(P709Error):
    pass


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _validate_release_sha(value: str) -> str:
    value = str(value).strip().lower()
    if not SHA40_RE.fullmatch(value):
        raise BoundaryError("repository release SHA must be a full lowercase 40-character Git SHA")
    return value


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BoundaryError(f"cannot read JSON evidence: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise BoundaryError("evidence JSON must be an object")
    return value


def _validate_evidence(scenario: str, evidence: Mapping[str, Any]) -> dict[str, Any]:
    if scenario not in SCENARIOS:
        raise BoundaryError(f"unknown scenario: {scenario}")
    if not isinstance(evidence, Mapping):
        raise BoundaryError("scenario evidence must be an object")

    expected = {**COMMON_FIELDS, **SCENARIO_FIELDS[scenario]}
    unknown = sorted(set(evidence) - set(expected))
    missing = sorted(set(expected) - set(evidence))
    if unknown:
        raise BoundaryError(f"unknown evidence fields for {scenario}: {unknown}")
    if missing:
        raise BoundaryError(f"missing evidence fields for {scenario}: {missing}")

    clean: dict[str, Any] = {}
    for key, spec in expected.items():
        value = evidence[key]
        if spec is bool:
            if type(value) is not bool:
                raise BoundaryError(f"{key} must be boolean")
        elif isinstance(spec, set):
            if not isinstance(value, str) or value not in spec:
                raise BoundaryError(f"{key} must be one of {sorted(spec)}")
        else:
            raise AssertionError(f"unsupported evidence spec for {key}")
        clean[key] = value

    if not clean["operator_attributable"]:
        raise BoundaryError("drill requires an attributable operator")
    if not clean["organization_scope_verified"]:
        raise BoundaryError("drill requires exact Organization scope verification")
    if clean["reusable_secret_exposed"]:
        raise BoundaryError("drill evidence must not expose reusable secrets")
    if clean["canonical_mutation_by_drill"]:
        raise BoundaryError("P7.09 drill evaluator cannot claim canonical mutation")
    if clean["external_effect_invoked_by_drill"]:
        raise BoundaryError("P7.09 drill evaluator cannot invoke an external effect")
    return clean


def _base_decision(scenario: str, decision: str, *, summary: str,
                   new_effect_authorization_required: bool,
                   governed_reentry_required: bool = True,
                   next_actions: tuple[str, ...] = ()) -> dict[str, Any]:
    return {
        "schema": DECISION_SCHEMA,
        "runbook_version": RUNBOOK_VERSION,
        "scenario": scenario,
        "decision": decision,
        "summary": summary,
        "operating_mode": OPERATING_MODE,
        "organization_scope": ORGANIZATION_SCOPE,
        "technical_recovery_only": True,
        "canonical_authority": False,
        "organizational_authority_satisfied": False,
        "consequential_approval_satisfied": False,
        "historical_external_effect_replay_authorized": False,
        "consequential_action_authorized_by_drill": False,
        "new_effect_authorization_required": new_effect_authorization_required,
        "governed_reentry_required": governed_reentry_required,
        "runbook_routes": list(RUNBOOK_ROUTES[scenario]),
        "next_actions": list(next_actions),
    }


def _runtime_crash(e: Mapping[str, Any]) -> dict[str, Any]:
    if e["historical_effect_replayed"]:
        return _base_decision(
            "runtime-crash", FAIL_CLOSED,
            summary="runtime recovery observed prohibited historical effect replay",
            new_effect_authorization_required=True,
            next_actions=("stop product/consequential processing", "reconcile affected execution/effects"),
        )
    if (
        e["runtime_status_after"] == "healthy"
        and e["exact_release_verified"]
        and e["supervised_generation_advanced"]
    ):
        return _base_decision(
            "runtime-crash", PASS,
            summary="supervised runtime recovered on the exact release without effect replay",
            new_effect_authorization_required=False,
            next_actions=("confirm P7.05 healthy state", "resume only through normal governed entrypoints"),
        )
    return _base_decision(
        "runtime-crash", FAIL_CLOSED,
        summary="runtime crash recovery is incomplete or release continuity is unverified",
        new_effect_authorization_required=False,
        next_actions=("keep consequential processing paused", "use P7.02/P7.05 diagnostics and bounded restart path"),
    )


def _mac_restart(e: Mapping[str, Any]) -> dict[str, Any]:
    if e["historical_effect_replayed"]:
        return _base_decision(
            "mac-restart", FAIL_CLOSED,
            summary="host restart observed prohibited historical effect replay",
            new_effect_authorization_required=True,
            next_actions=("stop consequential processing", "reconcile affected workflow/external effects"),
        )
    if (
        e["runtime_status_after"] == "healthy"
        and e["observer_loaded"]
        and e["exact_release_consistent"]
        and e["durable_state_integrity_verified"]
    ):
        return _base_decision(
            "mac-restart", PASS,
            summary="host restart preserved runtime, observer, exact release and durable-state integrity",
            new_effect_authorization_required=False,
            next_actions=("resume only through normal governed entrypoints",),
        )
    return _base_decision(
        "mac-restart", FAIL_CLOSED,
        summary="post-restart operating baseline is incomplete or unverified",
        new_effect_authorization_required=False,
        next_actions=("keep consequential processing paused", "verify P7.02, P7.05 and P7.03 state before reuse"),
    )


def _state_backup(e: Mapping[str, Any]) -> dict[str, Any]:
    if e["live_state_overwritten"]:
        return _base_decision(
            "persistent-state-or-backup-unavailable", FAIL_CLOSED,
            summary="live state was overwritten outside the admitted isolated P7.03 restore boundary",
            new_effect_authorization_required=True,
            next_actions=("stop processing", "preserve evidence", "perform explicit integrity/recovery review"),
        )
    if e["live_state_available"] and e["live_state_integrity_verified"]:
        return _base_decision(
            "persistent-state-or-backup-unavailable", PASS,
            summary="live durable state remains available and verifies; no restore is needed",
            new_effect_authorization_required=False,
            next_actions=("retain/verify backup according to runbook",),
        )
    if e["verified_backup_available"] and e["isolated_restore_verified"]:
        return _base_decision(
            "persistent-state-or-backup-unavailable", FORWARD_RECOVERY_REQUIRED,
            summary="isolated backup restore verifies, but P7.03 does not authorize overwriting live state",
            new_effect_authorization_required=True,
            next_actions=(
                "keep affected consequential processing paused",
                "use isolated restored state as recovery evidence only",
                "choose explicit forward/host recovery path before normal governed re-entry",
            ),
        )
    return _base_decision(
        "persistent-state-or-backup-unavailable", FAIL_CLOSED,
        summary="required durable state cannot be verified and no verified isolated recovery is available",
        new_effect_authorization_required=True,
        next_actions=("keep consequential processing paused", "locate and verify a valid backup or escalate to recovery review"),
    )


def _network(e: Mapping[str, Any]) -> dict[str, Any]:
    if e["historical_effect_replayed"]:
        return _base_decision(
            "network-proxy-tls-failure", FAIL_CLOSED,
            summary="network recovery observed prohibited historical effect replay",
            new_effect_authorization_required=True,
            next_actions=("stop retries", "reconcile the affected execution against authoritative evidence"),
        )
    effect = e["external_effect_state"]
    if effect == "unknown":
        return _base_decision(
            "network-proxy-tls-failure", RECONCILIATION_REQUIRED,
            summary="connectivity failure left the external effect outcome unknown",
            new_effect_authorization_required=True,
            next_actions=("do not retry the effect", "reconcile external/product outcome first"),
        )
    if not (e["connectivity_restored"] and e["tls_trust_verified"]):
        return _base_decision(
            "network-proxy-tls-failure", FAIL_CLOSED,
            summary="network/proxy/TLS trust is not fully restored and verified",
            new_effect_authorization_required=(effect != "none"),
            next_actions=("keep affected outbound work paused", "repair dependency/trust without weakening verification"),
        )
    if effect == "confirmed-succeeded":
        return _base_decision(
            "network-proxy-tls-failure", PASS,
            summary="dependency recovered and prior external effect is confirmed succeeded; replay remains prohibited",
            new_effect_authorization_required=False,
            next_actions=("record/reconstruct confirmed outcome", "do not repeat the historical effect"),
        )
    if effect == "confirmed-not-executed":
        return _base_decision(
            "network-proxy-tls-failure", PASS,
            summary="dependency recovered and prior effect is confirmed not executed",
            new_effect_authorization_required=True,
            next_actions=("re-enter the applicable governed workflow", "obtain/revalidate authorization for any new effect"),
        )
    return _base_decision(
        "network-proxy-tls-failure", PASS,
        summary="dependency recovered before any external effect occurred",
        new_effect_authorization_required=False,
        next_actions=("re-enter normal governed processing; technical recovery itself grants no effect authority",),
    )


def _product_host(e: Mapping[str, Any]) -> dict[str, Any]:
    if e["platform_bypass_used"]:
        return _base_decision(
            "product-host-unavailable", FAIL_CLOSED,
            summary="product-host outage was bypassed through an undeclared platform path",
            new_effect_authorization_required=True,
            next_actions=("stop bypass", "restore declared Product Contract boundary", "review hidden coupling"),
        )
    effect = e["external_effect_state"]
    if effect == "unknown":
        return _base_decision(
            "product-host-unavailable", RECONCILIATION_REQUIRED,
            summary="product-host outage left an external effect outcome unknown",
            new_effect_authorization_required=True,
            next_actions=("do not retry via platform or product", "reconcile outcome from authoritative retained evidence"),
        )
    if not (e["product_host_reachable"] and e["product_contract_boundary_available"]):
        return _base_decision(
            "product-host-unavailable", FAIL_CLOSED,
            summary="product host or declared Product Contract boundary remains unavailable",
            new_effect_authorization_required=(effect != "none"),
            next_actions=("keep dependent operation paused", "restore product-owned host/boundary without hidden coupling"),
        )
    if effect == "confirmed-succeeded":
        return _base_decision(
            "product-host-unavailable", PASS,
            summary="product boundary recovered and prior external effect is confirmed succeeded",
            new_effect_authorization_required=False,
            next_actions=("reconstruct/read confirmed evidence only", "never replay the historical effect"),
        )
    if effect == "confirmed-not-executed":
        return _base_decision(
            "product-host-unavailable", PASS,
            summary="product boundary recovered and prior effect is confirmed not executed",
            new_effect_authorization_required=True,
            next_actions=("re-enter applicable product/governed workflow for any new effect",),
        )
    return _base_decision(
        "product-host-unavailable", PASS,
        summary="product boundary recovered with no prior external effect",
        new_effect_authorization_required=False,
        next_actions=("resume only through the declared Product Contract surface",),
    )


def _uncertain_effect(e: Mapping[str, Any]) -> dict[str, Any]:
    if e["historical_effect_replayed"]:
        return _base_decision(
            "uncertain-external-effect", FAIL_CLOSED,
            summary="historical uncertain effect was replayed, violating the recovery boundary",
            new_effect_authorization_required=True,
            next_actions=("stop further effects", "preserve evidence", "perform explicit reconciliation"),
        )
    outcome = e["external_outcome"]
    if outcome == "unknown":
        return _base_decision(
            "uncertain-external-effect", RECONCILIATION_REQUIRED,
            summary="external outcome remains unknown; retry is prohibited",
            new_effect_authorization_required=True,
            next_actions=("preserve uncertainty", "reconcile against authoritative external/product evidence", "do not fabricate success/failure"),
        )
    if not e["reconciliation_evidence_verified"]:
        return _base_decision(
            "uncertain-external-effect", RECONCILIATION_REQUIRED,
            summary="an outcome is asserted but reconciliation evidence is not verified",
            new_effect_authorization_required=True,
            next_actions=("keep reconciliation-required state", "verify the authoritative outcome evidence"),
        )
    if outcome == "confirmed-succeeded":
        return _base_decision(
            "uncertain-external-effect", PASS,
            summary="uncertain outcome reconciled as succeeded; historical replay remains prohibited",
            new_effect_authorization_required=False,
            next_actions=("record/reconstruct confirmed outcome without replay",),
        )
    if not e["new_effect_authorized"]:
        return _base_decision(
            "uncertain-external-effect", PASS,
            summary="uncertain outcome reconciled as not executed; any future effect needs new authorization",
            new_effect_authorization_required=True,
            next_actions=("close the uncertain historical attempt", "obtain a new governed authorization before any new effect"),
        )
    return _base_decision(
        "uncertain-external-effect", PASS,
        summary="outcome reconciled as not executed and a separately authorized new effect may proceed through its governed path",
        new_effect_authorization_required=False,
        next_actions=("use a new execution/attempt identity", "do not mutate historical outcome evidence"),
    )


def _partial_evidence(e: Mapping[str, Any]) -> dict[str, Any]:
    if e["fabricated_replacement_evidence"]:
        return _base_decision(
            "partial-evidence-path", FAIL_CLOSED,
            summary="missing evidence was replaced with fabricated material",
            new_effect_authorization_required=True,
            next_actions=("discard fabricated material", "preserve provenance gap explicitly", "reconcile from retained authoritative evidence"),
        )
    if e["required_evidence_complete"] and e["integrity_verified"] and e["authoritative_source_known"]:
        return _base_decision(
            "partial-evidence-path", PASS,
            summary="required evidence path is complete, integrity-verified and attributable to a known source",
            new_effect_authorization_required=False,
            next_actions=("continue only with the verified evidence set",),
        )
    return _base_decision(
        "partial-evidence-path", FAIL_CLOSED,
        summary="required evidence path is incomplete, unverifiable or lacks an attributable source",
        new_effect_authorization_required=True,
        next_actions=("pause affected consequential processing", "recover/verify retained evidence without fabricating replacements"),
    )


def _credential(e: Mapping[str, Any]) -> dict[str, Any]:
    if e["organizational_authority_inferred_from_access"] or e["reusable_secret_in_evidence"]:
        return _base_decision(
            "credential-revocation-rotation", FAIL_CLOSED,
            summary="credential drill violated authority separation or secret minimization",
            new_effect_authorization_required=True,
            next_actions=("revoke exposed/unsafe credential", "remove secret from ordinary evidence", "re-establish least-privilege access"),
        )
    if e["old_credential_denied"] and e["replacement_credential_verified"] and e["exact_grant_scope_verified"]:
        return _base_decision(
            "credential-revocation-rotation", PASS,
            summary="old credential is denied and replacement remains limited to the exact grant",
            new_effect_authorization_required=False,
            next_actions=("retain only minimized credential lifecycle evidence", "remember operational access is not Organizational Authority"),
        )
    return _base_decision(
        "credential-revocation-rotation", FAIL_CLOSED,
        summary="credential lifecycle or exact grant scope is not verified",
        new_effect_authorization_required=False,
        next_actions=("deny affected access", "complete P7.04 revoke/rotate verification before reuse"),
    )


def _failed_update(e: Mapping[str, Any]) -> dict[str, Any]:
    if e["historical_effect_replayed"]:
        return _base_decision(
            "failed-update-rollback", FAIL_CLOSED,
            summary="deployment recovery observed prohibited historical product/external effect replay",
            new_effect_authorization_required=True,
            next_actions=("stop product processing", "reconcile affected execution/effects"),
        )
    if e["state_schema_changed"]:
        return _base_decision(
            "failed-update-rollback", FORWARD_RECOVERY_REQUIRED,
            summary="state schema changed; current P7.06 baseline does not admit automatic rollback after migration",
            new_effect_authorization_required=True,
            next_actions=("do not force rollback", "use explicit governed migration/forward-recovery review"),
        )
    if not (e["active_release_known"] and e["latest_transaction_known"]):
        return _base_decision(
            "failed-update-rollback", FAIL_CLOSED,
            summary="exact active release or latest deployment transaction cannot be established",
            new_effect_authorization_required=False,
            next_actions=("preserve interrupted evidence", "use P7.06 bounded forensics/recovery; do not guess release state"),
        )
    if not e["rollback_safe"]:
        return _base_decision(
            "failed-update-rollback", FORWARD_RECOVERY_REQUIRED,
            summary="latest deployment is not proven rollback-safe",
            new_effect_authorization_required=True,
            next_actions=("do not force rollback", "perform explicit forward-recovery disposition"),
        )
    if e["rollback_completed"] and e["runtime_healthy_after"] and e["observer_release_consistent"]:
        return _base_decision(
            "failed-update-rollback", PASS,
            summary="rollback restored a healthy exact-release runtime/observer unit without effect replay",
            new_effect_authorization_required=False,
            next_actions=("verify P7.03/P7.05 state", "resume only through normal governed entrypoints"),
        )
    return _base_decision(
        "failed-update-rollback", FAIL_CLOSED,
        summary="rollback is allowed but not complete or post-rollback health/release consistency is unverified",
        new_effect_authorization_required=False,
        next_actions=("keep affected runtime unavailable for consequential work", "complete P7.06 rollback/recovery verification"),
    )


EVALUATORS: dict[str, Callable[[Mapping[str, Any]], dict[str, Any]]] = {
    "runtime-crash": _runtime_crash,
    "mac-restart": _mac_restart,
    "persistent-state-or-backup-unavailable": _state_backup,
    "network-proxy-tls-failure": _network,
    "product-host-unavailable": _product_host,
    "uncertain-external-effect": _uncertain_effect,
    "partial-evidence-path": _partial_evidence,
    "credential-revocation-rotation": _credential,
    "failed-update-rollback": _failed_update,
}


def evaluate(scenario: str, evidence: Mapping[str, Any]) -> dict[str, Any]:
    clean = _validate_evidence(scenario, evidence)
    decision = EVALUATORS[scenario](clean)
    decision["evidence_classification"] = "operator-supplied bounded incident/drill facts; non-canonical"
    decision["evidence_fields"] = sorted(clean)
    return decision


def catalog() -> dict[str, Any]:
    result: dict[str, Any] = {
        "runbook_version": RUNBOOK_VERSION,
        "operating_mode": OPERATING_MODE,
        "scenarios": {},
    }
    for scenario in SCENARIOS:
        fields = {**COMMON_FIELDS, **SCENARIO_FIELDS[scenario]}
        rendered: dict[str, Any] = {}
        for key, spec in fields.items():
            rendered[key] = "boolean" if spec is bool else sorted(spec)
        result["scenarios"][scenario] = {
            "required_evidence": rendered,
            "runbook_routes": list(RUNBOOK_ROUTES[scenario]),
        }
    return result


def template(scenario: str) -> dict[str, Any]:
    if scenario not in SCENARIOS:
        raise BoundaryError(f"unknown scenario: {scenario}")
    fields = {**COMMON_FIELDS, **SCENARIO_FIELDS[scenario]}
    return {
        key: (
            None if spec is bool
            else next(iter(sorted(spec)))
        )
        for key, spec in fields.items()
    }


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise BoundaryError(f"refusing to overwrite existing drill evidence: {path}")
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        if os.name != "nt":
            os.fchmod(fd, 0o600)
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
        if os.name != "nt":
            os.chmod(path, 0o600)
    finally:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass


def record_drill(
    scenario: str,
    evidence: Mapping[str, Any],
    *,
    repository_sha: str,
    output_dir: Path,
    expected_decision: str,
) -> dict[str, Any]:
    repository_sha = _validate_release_sha(repository_sha)
    if expected_decision not in {PASS, FAIL_CLOSED, RECONCILIATION_REQUIRED, FORWARD_RECOVERY_REQUIRED}:
        raise BoundaryError("unsupported expected decision")
    decision = evaluate(scenario, evidence)
    receipt = {
        "schema": RECEIPT_SCHEMA,
        "status": "PASS" if decision["decision"] == expected_decision else "FAIL",
        "classification": "owner-local non-canonical P7.09 drill evidence",
        "runbook_version": RUNBOOK_VERSION,
        "repository_sha": repository_sha,
        "scenario": scenario,
        "expected_decision": expected_decision,
        "observed_decision": decision["decision"],
        "decision": decision,
        "technical_recovery_only": True,
        "canonical_authority": False,
        "organizational_authority_satisfied": False,
        "consequential_approval_satisfied": False,
        "historical_external_effect_replay_authorized": False,
        "external_effect_invoked_by_drill": False,
        "canonical_mutation_by_drill": False,
        "reusable_secret_emitted": False,
        "recorded_at": _utc_now(),
    }
    payload = (json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    base = f"p7-09-drill-{scenario}-{_stamp()}-{uuid.uuid4().hex[:8]}"
    output_dir = output_dir.expanduser().resolve()
    receipt_path = output_dir / f"{base}.json"
    digest_path = output_dir / f"{base}.json.sha256"
    _atomic_write(receipt_path, payload)
    _atomic_write(digest_path, f"{digest}  {receipt_path.name}\n".encode("ascii"))
    return {
        "status": receipt["status"],
        "scenario": scenario,
        "observed_decision": decision["decision"],
        "expected_decision": expected_decision,
        "receipt": str(receipt_path),
        "receipt_sha256": digest,
        "digest_file": str(digest_path),
    }


def verify_receipt(receipt_path: Path, digest_path: Path) -> dict[str, Any]:
    receipt_path = receipt_path.expanduser().resolve()
    digest_path = digest_path.expanduser().resolve()
    try:
        payload = receipt_path.read_bytes()
        digest_line = digest_path.read_text(encoding="ascii").strip()
    except OSError as exc:
        raise BoundaryError(f"cannot read receipt/digest: {exc}") from exc
    parts = digest_line.split()
    if len(parts) != 2 or parts[1] != receipt_path.name:
        raise BoundaryError("receipt digest sidecar shape/path mismatch")
    actual = hashlib.sha256(payload).hexdigest()
    if parts[0] != actual:
        raise BoundaryError("receipt SHA-256 mismatch")
    try:
        receipt = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise BoundaryError("receipt JSON invalid") from exc
    if not isinstance(receipt, dict) or receipt.get("schema") != RECEIPT_SCHEMA:
        raise BoundaryError("receipt schema invalid")
    if receipt.get("runbook_version") != RUNBOOK_VERSION:
        raise BoundaryError("receipt runbook version mismatch")
    if receipt.get("canonical_authority") is not False:
        raise BoundaryError("receipt cannot claim canonical authority")
    if receipt.get("historical_external_effect_replay_authorized") is not False:
        raise BoundaryError("receipt cannot authorize historical replay")
    if receipt.get("external_effect_invoked_by_drill") is not False:
        raise BoundaryError("receipt cannot contain an external-effect execution claim")
    if receipt.get("canonical_mutation_by_drill") is not False:
        raise BoundaryError("receipt cannot contain a canonical-mutation execution claim")
    return {
        "status": "PASS",
        "scenario": receipt.get("scenario"),
        "drill_status": receipt.get("status"),
        "receipt_sha256": actual,
        "canonical_authority": False,
        "historical_external_effect_replay_authorized": False,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    cat = sub.add_parser("catalog", help="print versioned P7.09 scenario catalog")
    cat.add_argument("--json", action="store_true")

    tmpl = sub.add_parser("template", help="print strict evidence template for a scenario")
    tmpl.add_argument("--scenario", choices=SCENARIOS, required=True)

    ev = sub.add_parser("evaluate", help="evaluate bounded incident/drill evidence without side effects")
    ev.add_argument("--scenario", choices=SCENARIOS, required=True)
    ev.add_argument("--evidence-json", type=Path, required=True)

    rec = sub.add_parser("record", help="evaluate and write non-canonical immutable drill receipt + SHA-256")
    rec.add_argument("--scenario", choices=SCENARIOS, required=True)
    rec.add_argument("--evidence-json", type=Path, required=True)
    rec.add_argument("--repository-sha", required=True)
    rec.add_argument("--output-dir", type=Path, required=True)
    rec.add_argument(
        "--expect-decision",
        choices=(PASS, FAIL_CLOSED, RECONCILIATION_REQUIRED, FORWARD_RECOVERY_REQUIRED),
        required=True,
    )

    ver = sub.add_parser("verify-receipt", help="verify P7.09 receipt SHA-256 and authority/replay invariants")
    ver.add_argument("--receipt", type=Path, required=True)
    ver.add_argument("--digest", type=Path, required=True)
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "catalog":
            value = catalog()
            if args.json:
                print(json.dumps(value, ensure_ascii=False, sort_keys=True))
            else:
                print(f"P7.09 runbook={RUNBOOK_VERSION} scenarios={len(SCENARIOS)}")
                for scenario in SCENARIOS:
                    print(f"- {scenario}")
            return 0
        if args.command == "template":
            print(json.dumps(template(args.scenario), ensure_ascii=False, sort_keys=True, indent=2))
            return 0
        if args.command == "evaluate":
            value = evaluate(args.scenario, _load_json(args.evidence_json))
            print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))
            return 0
        if args.command == "record":
            value = record_drill(
                args.scenario,
                _load_json(args.evidence_json),
                repository_sha=args.repository_sha,
                output_dir=args.output_dir,
                expected_decision=args.expect_decision,
            )
            print(json.dumps(value, ensure_ascii=False, sort_keys=True))
            return 0 if value["status"] == "PASS" else 2
        value = verify_receipt(args.receipt, args.digest)
        print(json.dumps(value, ensure_ascii=False, sort_keys=True))
        return 0
    except (P709Error, OSError, ValueError) as exc:
        print(f"P7.09 FAIL: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
