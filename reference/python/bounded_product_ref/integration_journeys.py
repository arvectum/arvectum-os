"""P5.04/R14 — bounded product use of the internal integration composition facade.

This module is product-owned executable evidence for the already-proved J1/J2
journeys. It deliberately imports exactly one Arvectum OS integration-facing
module and does not import runtime, capability, workspace, canonical-state or
operator-safety implementation modules directly.

R14 keeps governed provider/version evidence opaque to the product-owned helper
while requiring it to be supplied explicitly for every dependency-backed J1/J2
reliance. The facade remains the only platform import and delegates resolution to
the P5.03 semantic owner.

The facade remains internal/provisional. These helpers do not create product
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
    governed_versions: tuple[Any, ...],
) -> ProductFacadeReadEntry:
    """Enter J1 only through the integration facade.

    Product code does not reproduce capability admission, Product Contract
    continuity, provider compatibility, workspace authority or canonical-state
    rules. Current governed provider evidence is passed opaquely to the facade.
    """

    if not isinstance(facade, IntegrationCompositionFacade):
        raise TypeError("bounded product J1 requires IntegrationCompositionFacade")
    if not isinstance(capability_requests, tuple) or not capability_requests:
        raise ProductFacadeJourneyError("bounded product J1 requires explicit capability requests")
    if not isinstance(governed_versions, tuple):
        raise ProductFacadeJourneyError(
            "bounded product J1 requires explicit current governed dependency evidence"
        )

    admissions = tuple(
        facade.admit_capability(request, governed_versions=governed_versions)
        for request in capability_requests
    )
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
    governed_versions: tuple[Any, ...],
) -> Any:
    """Enter J2 only through the facade's Governed Execution choke point."""

    if not isinstance(facade, IntegrationCompositionFacade):
        raise TypeError("bounded product J2 requires IntegrationCompositionFacade")
    if not isinstance(governed_versions, tuple):
        raise ProductFacadeJourneyError(
            "bounded product J2 requires explicit current governed dependency evidence"
        )
    return facade.start_governed_execution(
        interaction=interaction,
        execution_id=execution_id,
        version_id=version_id,
        created_at=created_at,
        governed_versions=governed_versions,
    )
