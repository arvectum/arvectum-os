"""P5.08 — bounded product proof for workspace/capability integration adapters.

The product imports exactly one integration-facing Arvectum OS module and treats
all platform workspace/capability values as opaque. It does not import workspace,
capability, canonical-state, search, knowledge or audit implementation modules.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from arvectum_os_ref.integration_adapters import IntegrationAdapters


@dataclass(frozen=True, slots=True)
class ProductAdapterReadEntry:
    workspace: Any
    capability_admissions: tuple[Any, ...]


def enter_adapter_read_journey(
    *,
    adapters: IntegrationAdapters,
    capability_requests: tuple[Any, ...],
    governed_versions: tuple[Any, ...],
) -> ProductAdapterReadEntry:
    if not isinstance(adapters, IntegrationAdapters):
        raise TypeError("bounded product P5.08 journey requires IntegrationAdapters")
    if not isinstance(capability_requests, tuple) or not capability_requests:
        raise ValueError("bounded product P5.08 journey requires explicit capability requests")
    if not isinstance(governed_versions, tuple):
        raise ValueError("bounded product P5.08 journey requires current governed dependency evidence")

    admissions = tuple(
        adapters.capabilities.admit(request, governed_versions=governed_versions)
        for request in capability_requests
    )
    workspace = adapters.workspace.open()
    return ProductAdapterReadEntry(
        workspace=workspace,
        capability_admissions=admissions,
    )
