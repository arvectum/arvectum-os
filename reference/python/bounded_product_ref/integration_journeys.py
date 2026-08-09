"""P5.04 — bounded product use of the internal integration composition facade.

This module is product-owned executable evidence for the already-proved J1/J2
journeys.  It deliberately imports exactly one Arvectum OS integration-facing
module and does not import runtime, capability, workspace, canonical-state or
operator-safety implementation modules directly.

The facade remains internal/provisional.  These helpers do not create product
permission, organizational authority, a Stable Product Contract or a public SDK.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from arvectum_os_ref.integration_composition import IntegrationCompositionFacade


class ProductFacadeJourneyError(ValueError):
    """The bounded product cannot continue through the composed facade boundary."""


@dataclass(frozen=True, slots=True)
class ProductFacadeReadEntry:
    """Product-owned J1 entry evidence; platform values remain opaque here."""

    workspace: Any
    capability_admissions: tuple[Any, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.capability_admissions, tuple) or not self.capability_admissions:
            raise ValueError("facade read entry requires at least one admitted dependency")


def enter_facade_read_journey(
    *,
    facade: IntegrationCompositionFacade,
    capability_requests: tuple[Any, ...],
) -> ProductFacadeReadEntry:
    """Enter J1 only through the integration facade.

    Product code does not reproduce capability admission, Product Contract
    continuity, workspace authority or canonical-state rules.  The facade delegates
    those responsibilities to the existing shared semantic owners.
    """

    if not isinstance(facade, IntegrationCompositionFacade):
        raise TypeError("bounded product J1 requires IntegrationCompositionFacade")
    if not isinstance(capability_requests, tuple) or not capability_requests:
        raise ProductFacadeJourneyError("bounded product J1 requires explicit capability requests")

    admissions = tuple(facade.admit_capability(request) for request in capability_requests)
    workspace = facade.open_workspace()
    return ProductFacadeReadEntry(
        workspace=workspace,
        capability_admissions=admissions,
    )


def start_facade_action_journey(
    *,
    facade: IntegrationCompositionFacade,
    interaction: Any,
    execution_id: Any,
    version_id: Any,
    created_at: datetime,
) -> Any:
    """Enter J2 only through the facade's Governed Execution choke point."""

    if not isinstance(facade, IntegrationCompositionFacade):
        raise TypeError("bounded product J2 requires IntegrationCompositionFacade")
    return facade.start_governed_execution(
        interaction=interaction,
        execution_id=execution_id,
        version_id=version_id,
        created_at=created_at,
    )
