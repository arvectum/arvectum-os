"""P5.08/R15 — bounded product proof for integration adapters.

The product imports exactly one integration-facing Arvectum OS module and treats
all platform workspace/capability values as opaque. R15 makes workspace reliance
an explicit product-owned opt-in instead of assuming every integration carries a
workspace binding.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from arvectum_os_ref.integration_adapters import (
    IntegrationAdapters,
    compose_workspace_adapter,
)


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
        raise TypeError("bounded product integration journey requires IntegrationAdapters")
    if not isinstance(capability_requests, tuple) or not capability_requests:
        raise ValueError("bounded product integration journey requires explicit capability requests")
    if not isinstance(governed_versions, tuple):
        raise ValueError("bounded product integration journey requires current governed dependency evidence")

    admissions = tuple(
        adapters.capabilities.admit(request, governed_versions=governed_versions)
        for request in capability_requests
    )
    workspace = compose_workspace_adapter(adapters=adapters).open()
    return ProductAdapterReadEntry(
        workspace=workspace,
        capability_admissions=admissions,
    )
