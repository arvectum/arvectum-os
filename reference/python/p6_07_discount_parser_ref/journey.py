"""P6.07 product-facing reconstruction journey.

This deliberately tiny module is the product/platform seam for the Stage 1 proof.
It uses only the shared integration adapter boundary. Product-domain schemas,
platform capability internals, event stores and workspace internals are not
imported here.
"""

from __future__ import annotations

from typing import Any

from arvectum_os_ref.integration_adapters import IntegrationAdapters


class P607IntegrationContinuityError(RuntimeError):
    """P6.07 evidence lost exact Product Contract continuity."""


def reconstruct_publication(
    *,
    adapters: IntegrationAdapters,
    request: Any,
    governed_versions: tuple[Any, ...] | None,
    manifest: Any,
    evidence_constraints: tuple[Any, ...],
):
    """Reconstruct one Discount Parser publication execution through CAP-004.

    P6.06 requires this product to reconstruct its own governed publication under
    the exact effective Product Contract version. The shared CAP-004 capability is
    intentionally generic and can also inspect other products' evidence, so this
    product-specific continuity guard belongs here rather than in the platform.
    """

    if not isinstance(adapters, IntegrationAdapters):
        raise TypeError("P6.07 reconstruction requires IntegrationAdapters")
    if manifest is None or getattr(manifest, "product_contract", None) is None:
        raise P607IntegrationContinuityError(
            "P6.07 publication reconstruction requires an exact Product Contract Version pin"
        )
    if manifest.product_contract != adapters.facade.context.product_contract:
        raise P607IntegrationContinuityError(
            "P6.07 publication evidence does not match the composed Product Contract Version"
        )

    return adapters.capabilities.reconstruct_execution(
        request=request,
        governed_versions=governed_versions,
        manifest=manifest,
        evidence_constraints=evidence_constraints,
    )
