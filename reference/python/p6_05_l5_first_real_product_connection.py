#!/usr/bin/env python3
"""P6.05-L5 minimal read-only local connection/preflight layer.

This module connects an existing P6.05-L4 Organization/operator context
with the exact P6.02 Product Contract projection.

It proves composition compatibility without creating persistent state
or performing external actions.
"""

from __future__ import annotations

import hashlib
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Final, Sequence

from arvectum_os_ref.canonical import AuthorityMode
from arvectum_os_ref.integration_adapters import IntegrationAdapters, compose_integration_adapters
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_004_AUDIT_RECONSTRUCTION,
)
from arvectum_os_ref.product_contract import (
    ProductContract,
    ProductContractLifecycle,
)
from arvectum_os_ref.product_contract_resolution import (
    DependencySupportDisposition,
    GovernedDependencyVersionEvidence,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from p6_03_tender_operator_ref.contract import (
    DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
    PRODUCT_COMPATIBILITY_LINE,
)
from p6_05_l4_operator_context_preflight import inspect_operator_context_file
from p6_05_tender_attachment_ref.contract import (
    P6_02_CANONICAL_BLOB_SHA,
    P6_02_CANONICAL_CONTRACT_PATH,
    P6_02_CONTRACT_SUBJECT_VALUE,
    P6_02_CONTRACT_VERSION_VALUE,
    P6_05_PROJECTION_SUBJECT_VALUE,
    P605ExecutableProductContractProjection,
    build_p6_05_product_contract_projection,
    p6_02_canonical_version_pin,
)

GOVERNANCE_REFERENCE: Final = "docs/contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md@1.0.0"


class L5Error(str, Enum):
    CANONICAL_PRODUCT_CONTRACT_SOURCE_MISMATCH = "CANONICAL_PRODUCT_CONTRACT_SOURCE_MISMATCH"
    PROJECTION_SOURCE_BOUNDARY_LOST = "PROJECTION_SOURCE_BOUNDARY_LOST"
    WRONG_PRODUCT_CONTRACT_SUBJECT = "WRONG_PRODUCT_CONTRACT_SUBJECT"
    WRONG_PRODUCT_CONTRACT_VERSION_IDENTITY = "WRONG_PRODUCT_CONTRACT_VERSION_IDENTITY"
    WRONG_PRODUCT_CONTRACT_LIFECYCLE = "WRONG_PRODUCT_CONTRACT_LIFECYCLE"
    WRONG_PRODUCT_COMPATIBILITY_LINE = "WRONG_PRODUCT_COMPATIBILITY_LINE"
    ORGANIZATION_MISMATCH = "ORGANIZATION_MISMATCH"
    DEPENDENCY_SET_MISMATCH = "DEPENDENCY_SET_MISMATCH"
    DEPENDENCY_VERSION_MISMATCH = "DEPENDENCY_VERSION_MISMATCH"
    EXTERNAL_AUTHORITY_DECLARATION_LOST = "EXTERNAL_AUTHORITY_DECLARATION_LOST"
    CONNECTION_FAILED = "CONNECTION_FAILED"


class L5ConnectionError(Exception):
    """Typed error for explicit L5 preflight continuity guards."""
    def __init__(self, code: L5Error):
        self.code = code
        super().__init__(code.value)


@dataclass(frozen=True, slots=True)
class ConnectionResult:
    """Ephemeral L5 connection result held in memory only."""
    organization_scope: OrganizationScope
    principal: Principal
    actor_context: ActorContext
    product_contract: ProductContract
    adapters: IntegrationAdapters
    connected_at: datetime
    external_authority_preserved: bool
    canonical_source_verified: bool


def _git_blob_sha(path: Path) -> str:
    """Calculate Git object blob SHA without git subprocess."""
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def _verify_canonical_source(repo_root: Path) -> None:
    source_file = repo_root / P6_02_CANONICAL_CONTRACT_PATH
    if source_file.is_symlink():
        raise L5ConnectionError(L5Error.CANONICAL_PRODUCT_CONTRACT_SOURCE_MISMATCH)
    if not source_file.is_file():
        raise L5ConnectionError(L5Error.CANONICAL_PRODUCT_CONTRACT_SOURCE_MISMATCH)
    try:
        resolved = source_file.resolve(strict=True)
        resolved.relative_to(repo_root)
    except (ValueError, OSError) as exc:
        raise L5ConnectionError(L5Error.CANONICAL_PRODUCT_CONTRACT_SOURCE_MISMATCH) from exc

    try:
        blob_sha = _git_blob_sha(resolved)
    except OSError as exc:
        raise L5ConnectionError(L5Error.CANONICAL_PRODUCT_CONTRACT_SOURCE_MISMATCH) from exc

    if blob_sha != P6_02_CANONICAL_BLOB_SHA:
        raise L5ConnectionError(L5Error.CANONICAL_PRODUCT_CONTRACT_SOURCE_MISMATCH)


def connect_product(
    state_file: Path,
    *,
    arvectum_repo_root: Path | None = None,
) -> tuple[int, tuple[str, ...], ConnectionResult | None]:
    """Connect existing L4 context to P6.02 product boundary.

    The Product Contract objects produced by this module are non-authoritative
    executable projections of the canonical P6.02 declaration. They do not
    represent the authoritative Canonical Product Contract Record and their
    creation metadata (Actor/time) is projected for runtime use only.
    """

    # 1. Inspect L4 context (read-only)
    rc, l4_lines, bootstrap_result = inspect_operator_context_file(
        state_file,
        arvectum_repo_root=arvectum_repo_root
    )

    if rc != 0 or bootstrap_result is None:
        # Failure in L4 preflight
        l4_failure_code = "UNKNOWN"
        for line in l4_lines:
            if line.startswith("failure_code="):
                l4_failure_code = line.split("=")[1]
                break
        return rc, tuple(_safe_summary(status="FAIL", failure_code=l4_failure_code)), None

    org_scope = bootstrap_result.organization_scope
    principal = bootstrap_result.principal
    actor_context = bootstrap_result.actor_context

    repo_root = (
        arvectum_repo_root or Path(__file__).resolve().parents[2]
    ).resolve(strict=True)

    try:
        # 2. Verify immutable canonical P6.02 source
        _verify_canonical_source(repo_root)

        # 3. Build non-authoritative executable projection of P6.02 0.1.0 contract
        connected_at = datetime.now(timezone.utc)
        contract = build_p6_05_product_contract_projection(
            actor=actor_context,
            created_at=connected_at
        )

        # 4. Continuity check on the canonical source pin and projection boundary
        try:
            pin = contract.version_pin
            
            # scope == real L4 Organization
            if pin.subject_id.scope != org_scope.organization_id.value or pin.version_id.scope != org_scope.organization_id.value:
                raise L5ConnectionError(L5Error.ORGANIZATION_MISMATCH)
            
            # Organization continuity
            if contract.organization != org_scope:
                raise L5ConnectionError(L5Error.ORGANIZATION_MISMATCH)

            # Require exact canonical P6.02 pin
            if pin.subject_id.namespace != "product-contract-subject":
                raise L5ConnectionError(L5Error.WRONG_PRODUCT_CONTRACT_SUBJECT)
            if pin.subject_id.value != P6_02_CONTRACT_SUBJECT_VALUE:
                raise L5ConnectionError(L5Error.WRONG_PRODUCT_CONTRACT_SUBJECT)
            if pin.version_id.namespace != "product-contract-version":
                raise L5ConnectionError(L5Error.WRONG_PRODUCT_CONTRACT_VERSION_IDENTITY)
            if pin.version_id.value != P6_02_CONTRACT_VERSION_VALUE:
                raise L5ConnectionError(L5Error.WRONG_PRODUCT_CONTRACT_VERSION_IDENTITY)
            if pin.semantic_type != "platform.product-contract":
                raise L5ConnectionError(L5Error.PROJECTION_SOURCE_BOUNDARY_LOST)
            if pin.authority_scope != "platform.product-contract/boundary":
                raise L5ConnectionError(L5Error.PROJECTION_SOURCE_BOUNDARY_LOST)
            if pin.lifecycle_status != ProductContractLifecycle.PROVISIONAL.value:
                raise L5ConnectionError(L5Error.WRONG_PRODUCT_CONTRACT_LIFECYCLE)
            
            # product compatibility line
            if contract.product_version != PRODUCT_COMPATIBILITY_LINE:
                raise L5ConnectionError(L5Error.WRONG_PRODUCT_COMPATIBILITY_LINE)

            # Require distinct projection record identity
            if contract.record.subject_id == pin.subject_id or contract.record.version_id == pin.version_id:
                raise L5ConnectionError(L5Error.PROJECTION_SOURCE_BOUNDARY_LOST)
            if contract.record.subject_id.value != P6_05_PROJECTION_SUBJECT_VALUE:
                raise L5ConnectionError(L5Error.PROJECTION_SOURCE_BOUNDARY_LOST)
                
            if not isinstance(contract, P605ExecutableProductContractProjection):
                raise L5ConnectionError(L5Error.PROJECTION_SOURCE_BOUNDARY_LOST)
            if (
                contract.canonical_source_path != P6_02_CANONICAL_CONTRACT_PATH
                or contract.canonical_source_blob_sha != P6_02_CANONICAL_BLOB_SHA
            ):
                raise L5ConnectionError(L5Error.PROJECTION_SOURCE_BOUNDARY_LOST)

        except (AttributeError, IndexError, TypeError) as exc:
            if isinstance(exc, L5ConnectionError):
                raise
            raise L5ConnectionError(L5Error.CONNECTION_FAILED) from exc

        # 5. Form explicit provider evidence for CAP-001@1.0.0 and CAP-004@1.0.0
        governed_versions = (
            GovernedDependencyVersionEvidence(
                dependency_id=CAP_001_DOCUMENT_ARTIFACT,
                contract_version="1.0.0",
                disposition=DependencySupportDisposition.SUPPORTED,
                governance_reference=GOVERNANCE_REFERENCE,
            ),
            GovernedDependencyVersionEvidence(
                dependency_id=CAP_004_AUDIT_RECONSTRUCTION,
                contract_version="1.0.0",
                disposition=DependencySupportDisposition.SUPPORTED,
                governance_reference=GOVERNANCE_REFERENCE,
            ),
        )

        # 6. Verify exact dependency set and version matches CAP-001 + CAP-004 @ 1.0.0 only
        actual_deps = {dep.dependency_id for dep in contract.dependencies}
        expected_deps = {CAP_001_DOCUMENT_ARTIFACT, CAP_004_AUDIT_RECONSTRUCTION}
        if actual_deps != expected_deps:
            raise L5ConnectionError(L5Error.DEPENDENCY_SET_MISMATCH)

        for dep in contract.dependencies:
            if dep.contract_version != "1.0.0":
                raise L5ConnectionError(L5Error.DEPENDENCY_VERSION_MISMATCH)

        # 7. Verify External Authority continuity for documents BEFORE composition
        document_accesses = []
        for op in contract.operations:
            for access in op.canonical_accesses:
                if access.semantic_type == "platform.document":
                    document_accesses.append(access)
        
        if not document_accesses:
            raise L5ConnectionError(L5Error.EXTERNAL_AUTHORITY_DECLARATION_LOST)
            
        for access in document_accesses:
            if access.authority_mode is not AuthorityMode.EXTERNAL_REFERENCE:
                raise L5ConnectionError(L5Error.EXTERNAL_AUTHORITY_DECLARATION_LOST)
            if access.authority_scope != DOCUMENT_EXTERNAL_AUTHORITY_SCOPE:
                raise L5ConnectionError(L5Error.EXTERNAL_AUTHORITY_DECLARATION_LOST)

        # 8. Compose integration adapters using canonical source pin
        expected_pin = p6_02_canonical_version_pin(organization=org_scope)
        try:
            adapters = compose_integration_adapters(
                contract=contract,
                actor=actor_context,
                effective_product_contract=expected_pin,
                governed_versions=governed_versions,
            )
        except Exception as exc:
            if isinstance(exc, L5ConnectionError):
                raise
            raise L5ConnectionError(L5Error.CONNECTION_FAILED) from exc

        if adapters.facade.context.product_contract != expected_pin:
            raise L5ConnectionError(L5Error.PROJECTION_SOURCE_BOUNDARY_LOST)

        result = ConnectionResult(
            organization_scope=org_scope,
            principal=principal,
            actor_context=actor_context,
            product_contract=contract,
            adapters=adapters,
            connected_at=connected_at,
            external_authority_preserved=True,
            canonical_source_verified=True,
        )

        return 0, tuple(_safe_summary(status="PASS", result=result)), result

    except L5ConnectionError as exc:
        return 1, tuple(_safe_summary(status="FAIL", failure_code=exc.code.value)), None
    except Exception:
        return 1, tuple(_safe_summary(status="FAIL", failure_code=L5Error.CONNECTION_FAILED.value)), None


def _safe_summary(
    status: str,
    result: ConnectionResult | None = None,
    failure_code: str | None = None
) -> list[str]:
    if status == "PASS" and result:
        # Pass summary formed from verified values
        contract = result.product_contract
        pin = contract.version_pin
        cap001_ver = "unknown"
        cap004_ver = "unknown"
        for dep in contract.dependencies:
            if dep.dependency_id == CAP_001_DOCUMENT_ARTIFACT:
                cap001_ver = dep.contract_version
            elif dep.dependency_id == CAP_004_AUDIT_RECONSTRUCTION:
                cap004_ver = dep.contract_version

        from arvectum_os_ref.product_capability_consumption import CAP_002_MEMORY_KNOWLEDGE, CAP_003_SEARCH_PROJECTION
        cap002_present = any(d.dependency_id == CAP_002_MEMORY_KNOWLEDGE for d in contract.dependencies)
        cap003_present = any(d.dependency_id == CAP_003_SEARCH_PROJECTION for d in contract.dependencies)

        return [
            "p6_05_l5_status=PASS",
            "",
            "organization_context=configured",
            "operator_principal=configured",
            "actor_context=configured",
            "product_context=configured",
            "",
            "product_contract=0.1.0",
            "product_contract_projection=non_authoritative",
            "canonical_source_verified=true",
            "",
            f"organization_continuity={str(result.organization_scope == contract.organization).lower()}",
            f"actor_organization_continuity={str(result.actor_context.organization == contract.organization).lower()}",
            f"product_organization_continuity={str(contract.product_id.scope == contract.organization.organization_id.value).lower()}",
            f"product_contract_organization_continuity={str(pin.subject_id.scope == contract.organization.organization_id.value).lower()}",
            "",
            "cap_001=configured",
            f"cap_001_contract_version={cap001_ver}",
            "cap_004=configured",
            f"cap_004_contract_version={cap004_ver}",
            "",
            f"cap_002_present={str(cap002_present).lower()}",
            f"cap_003_present={str(cap003_present).lower()}",
            "",
            "authorization_grants_created=false",
            "delegations_created=false",
            "organizational_authority_created=false",
            "",
            f"external_authority_preserved={str(result.external_authority_preserved).lower()}",
            "product_semantics_platformized=false",
            "",
            "canonical_mutation=false",
            "eis_invoked=false",
            "soap_invoked=false",
            "network_product_runtime_invoked=false",
            "external_actions=false",
        ]
    else:
        return [
            "p6_05_l5_status=FAIL",
            f"failure_code={failure_code or 'UNKNOWN'}",
            "organization_context=not_proven",
            "operator_principal=not_proven",
            "actor_context=not_proven",
            "product_context=not_proven",
            "product_contract=not_proven",
            "product_contract_projection=not_proven",
            "canonical_source_verified=not_proven",
            "organization_continuity=not_proven",
            "actor_organization_continuity=not_proven",
            "product_organization_continuity=not_proven",
            "product_contract_organization_continuity=not_proven",
            "cap_001=not_proven",
            "cap_004=not_proven",
            "cap_002_present=not_proven",
            "cap_003_present=not_proven",
            "authorization_grants_created=false",
            "delegations_created=false",
            "organizational_authority_created=false",
            "external_authority_preserved=not_proven",
            "product_semantics_platformized=false",
            "canonical_mutation=false",
            "eis_invoked=false",
            "soap_invoked=false",
            "network_product_runtime_invoked=false",
            "external_actions=false",
        ]


def main(argv: Sequence[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="P6.05-L5 First real product connection preflight.")
    parser.add_argument("--state-file", required=True, type=Path)
    args = parser.parse_args(argv)

    rc, lines, _ = connect_product(args.state_file)
    for line in lines:
        print(line)
    return rc

if __name__ == "__main__":
    sys.exit(main())
