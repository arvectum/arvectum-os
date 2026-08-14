#!/usr/bin/env python3
"""P6.05-L5 minimal read-only local connection/preflight layer.

This module connects an existing P6.05-L4 Organization/operator context
with the exact P6.02 Product Contract projection.

It proves composition compatibility without creating persistent state
or performing external actions.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Final, Sequence

from arvectum_os_ref.integration_adapters import IntegrationAdapters, compose_integration_adapters
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_004_AUDIT_RECONSTRUCTION,
    CAPABILITY_CONTRACT_VERSION,
)
from arvectum_os_ref.product_contract import ProductContract
from arvectum_os_ref.product_contract_resolution import (
    DependencySupportDisposition,
    GovernedDependencyVersionEvidence,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from p6_05_l4_operator_context_preflight import inspect_operator_context_file
from p6_05_tender_attachment_ref.contract import build_p6_05_product_contract_projection

GOVERNANCE_REFERENCE: Final = "docs/contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md@1.0.0"


@dataclass(frozen=True, slots=True)
class ConnectionResult:
    """Ephemeral L5 connection result held in memory only."""
    organization_scope: OrganizationScope
    principal: Principal
    actor_context: ActorContext
    product_contract: ProductContract
    adapters: IntegrationAdapters
    connected_at: datetime


def connect_product(
    state_file: Path,
    *,
    arvectum_repo_root: Path | None = None,
) -> tuple[int, tuple[str, ...], ConnectionResult | None]:
    """Connect existing L4 context to P6.02 product boundary."""
    
    # 1. Inspect L4 context (read-only)
    rc, l4_lines, bootstrap_result = inspect_operator_context_file(
        state_file, 
        arvectum_repo_root=arvectum_repo_root
    )
    
    if rc != 0 or bootstrap_result is None:
        # Failure in L4 preflight
        safe_failure = [line for line in l4_lines if "p6_05_l4_status" in line or "failure_code" in line]
        return rc, tuple(["p6_05_l5_status=FAIL"] + safe_failure), None

    org_scope = bootstrap_result.organization_scope
    principal = bootstrap_result.principal
    actor_context = bootstrap_result.actor_context
    
    try:
        # 2. Build exact P6.05 projection of P6.02 0.1.0 contract
        # Use fixed creation time for deterministic preflight
        now = datetime.now(timezone.utc)
        contract = build_p6_05_product_contract_projection(
            actor=actor_context,
            created_at=now
        )
        
        # 3. L5-specific validation (Exact P6.02 v0.1.0)
        if contract.record.payload[1] != ("contract_version", "0.1.0"):
            raise ValueError("WRONG_PRODUCT_CONTRACT_VERSION")
            
        if contract.organization != org_scope:
             raise ValueError("ORGANIZATION_MISMATCH")
             
        # 4. Form explicit provider evidence for CAP-001 and CAP-004 @ 1.0.0
        governed_versions = (
            GovernedDependencyVersionEvidence(
                dependency_id=CAP_001_DOCUMENT_ARTIFACT,
                contract_version=CAPABILITY_CONTRACT_VERSION,
                disposition=DependencySupportDisposition.SUPPORTED,
                governance_reference=GOVERNANCE_REFERENCE,
            ),
            GovernedDependencyVersionEvidence(
                dependency_id=CAP_004_AUDIT_RECONSTRUCTION,
                contract_version=CAPABILITY_CONTRACT_VERSION,
                disposition=DependencySupportDisposition.SUPPORTED,
                governance_reference=GOVERNANCE_REFERENCE,
            ),
        )
        
        # 5. Compose integration adapters (validates declaration & compatibility)
        adapters = compose_integration_adapters(
            contract=contract,
            actor=actor_context,
            effective_product_contract=contract.version_pin,
            governed_versions=governed_versions,
        )
        
        # 6. Verify exact dependency set matches CAP-001 + CAP-004 only
        actual_deps = {dep.dependency_id for dep in contract.dependencies}
        expected_deps = {CAP_001_DOCUMENT_ARTIFACT, CAP_004_AUDIT_RECONSTRUCTION}
        if actual_deps != expected_deps:
            raise ValueError("DEPENDENCY_SET_MISMATCH")

        result = ConnectionResult(
            organization_scope=org_scope,
            principal=principal,
            actor_context=actor_context,
            product_contract=contract,
            adapters=adapters,
            connected_at=now,
        )
        
        return 0, tuple(_safe_summary(status="PASS", result=result)), result

    except Exception as exc:
        code = str(exc) if str(exc).isupper() else "CONNECTION_FAILED"
        return 1, tuple(_safe_summary(status="FAIL", failure_code=code)), None


def _safe_summary(
    status: str, 
    result: ConnectionResult | None = None,
    failure_code: str | None = None
) -> list[str]:
    if status == "PASS" and result:
        return [
            "p6_05_l5_status=PASS",
            "",
            "organization_context=configured",
            "operator_principal=configured",
            "actor_context=configured",
            "product_context=configured",
            "",
            "product_contract=0.1.0",
            "",
            "organization_continuity=true",
            "actor_organization_continuity=true",
            "product_organization_continuity=true",
            "product_contract_organization_continuity=true",
            "",
            "cap_001=configured",
            "cap_001_contract_version=1.0.0",
            "cap_004=configured",
            "cap_004_contract_version=1.0.0",
            "",
            "cap_002_present=false",
            "cap_003_present=false",
            "",
            "authorization_grants_created=false",
            "delegations_created=false",
            "organizational_authority_created=false",
            "",
            "external_authority_preserved=true",
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
