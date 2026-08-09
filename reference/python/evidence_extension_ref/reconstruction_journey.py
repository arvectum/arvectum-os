"""P5.09 — materially distinct read-only integration journey.

The extension imports exactly one integration-facing Arvectum OS module. Platform
reconstruction values are passed through opaquely; this extension does not import
CAP-004, Event/provenance, workspace, canonical-state or execution internals.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from arvectum_os_ref.integration_adapters import IntegrationAdapters


@dataclass(frozen=True, slots=True)
class EvidenceInspectionEntry:
    """Extension-owned entry result; the reconstruction object remains platform-owned."""

    reconstruction: Any
    inspection_mode: str = "read-only-governed-evidence"


def inspect_execution_evidence(
    *,
    adapters: IntegrationAdapters,
    request: Any,
    governed_versions: tuple[Any, ...] | None,
    manifest: Any,
    evidence_constraints: tuple[Any, ...],
) -> EvidenceInspectionEntry:
    """Inspect one governed reconstruction through the same P5.08 adapter seam."""

    if not isinstance(adapters, IntegrationAdapters):
        raise TypeError("P5.09 evidence extension requires IntegrationAdapters")
    if not isinstance(evidence_constraints, tuple):
        raise ValueError("P5.09 evidence extension requires explicit immutable evidence constraints")

    reconstruction = adapters.capabilities.reconstruct_execution(
        request=request,
        governed_versions=governed_versions,
        manifest=manifest,
        evidence_constraints=evidence_constraints,
    )
    return EvidenceInspectionEntry(reconstruction=reconstruction)
