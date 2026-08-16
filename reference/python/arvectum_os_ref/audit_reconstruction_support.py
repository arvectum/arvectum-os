"""P3.06 — bounded Audit / Reconstruction Support candidate slice.

CAP-004 is read-oriented and derived. It resolves exact governed evidence already
produced by Core Runtime and RFC-0006 semantics; it does not create authority,
repair missing history, replay side effects, or select a logging/SIEM/storage
technology. Product compliance narratives and UX remain product-owned.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .event_provenance import ReconstructionManifest
from .execution import GovernedVersionPin
from .identity import Identity
from .security import OrganizationScope


class EvidenceAvailability(str, Enum):
    AVAILABLE = "Available"
    REDACTED = "Redacted"
    DELETED = "Deleted"
    UNAVAILABLE = "Unavailable"
    MISSING = "Missing"


class AuditReconstructionError(ValueError):
    """Supplied reconstruction evidence or access context is inconsistent."""


@dataclass(frozen=True, slots=True)
class EvidenceDisposition:
    """Current visibility/retention state for one exact governed evidence version."""

    version_id: Identity
    availability: EvidenceAvailability
    reason: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.version_id, Identity):
            raise AuditReconstructionError("evidence disposition requires an exact Version Identity")
        if not isinstance(self.availability, EvidenceAvailability):
            raise AuditReconstructionError("evidence availability must be explicit")
        if self.availability is EvidenceAvailability.AVAILABLE:
            if self.reason is not None:
                raise AuditReconstructionError("available evidence must not carry an unavailability reason")
        elif not isinstance(self.reason, str) or not self.reason.strip():
            raise AuditReconstructionError("non-available evidence requires an explicit bounded reason")


@dataclass(frozen=True, slots=True)
class AuditEvidenceItem:
    """One derived reconstruction item; source authority remains with the governed pin."""

    role: str
    availability: EvidenceAvailability
    source: GovernedVersionPin | None
    version_id: Identity
    reason: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.role, str) or not self.role.strip():
            raise AuditReconstructionError("audit evidence role must be explicit")
        if not isinstance(self.version_id, Identity):
            raise AuditReconstructionError("audit evidence must preserve exact Version Identity")
        if self.availability is EvidenceAvailability.AVAILABLE:
            if self.source is None or self.source.version_id != self.version_id:
                raise AuditReconstructionError("available audit evidence must expose its exact governed source pin")
            if self.reason is not None:
                raise AuditReconstructionError("available audit evidence must not carry a reason")
        else:
            if self.source is not None:
                raise AuditReconstructionError("restricted/unavailable evidence must not leak its governed source pin")
            if not isinstance(self.reason, str) or not self.reason.strip():
                raise AuditReconstructionError("restricted/unavailable evidence must explain its state")


@dataclass(frozen=True, slots=True)
class AuditReconstructionView:
    """Derived read-only view of one exact governed execution reconstruction."""

    organization: OrganizationScope
    execution_subject_id: Identity
    initiating_actor_id: Identity
    operation_name: str
    evidence: tuple[AuditEvidenceItem, ...]
    correlation_refs: tuple[Identity, ...]
    causation_refs: tuple[Identity, ...]
    complete: bool

    def __post_init__(self) -> None:
        if not isinstance(self.organization, OrganizationScope):
            raise AuditReconstructionError("audit reconstruction Organization scope must be explicit")
        if not isinstance(self.execution_subject_id, Identity):
            raise AuditReconstructionError("audit reconstruction Execution Identity must be explicit")
        if not isinstance(self.initiating_actor_id, Identity):
            raise AuditReconstructionError("audit reconstruction actor attribution must be explicit")
        if not isinstance(self.operation_name, str) or not self.operation_name.strip():
            raise AuditReconstructionError("audit reconstruction operation must be explicit")
        if not isinstance(self.evidence, tuple) or not self.evidence:
            raise AuditReconstructionError("audit reconstruction requires explicit evidence items")
        if any(not isinstance(item, AuditEvidenceItem) for item in self.evidence):
            raise AuditReconstructionError("audit reconstruction evidence items must be typed")
        if len({(item.role, item.version_id) for item in self.evidence}) != len(self.evidence):
            raise AuditReconstructionError("audit reconstruction must not duplicate (role, version) pairs")

        # Consistent availability/source for any reused version_id
        version_dispositions: dict[Identity, tuple[EvidenceAvailability, GovernedVersionPin | None]] = {}
        for item in self.evidence:
            prior = version_dispositions.get(item.version_id)
            if prior is None:
                version_dispositions[item.version_id] = (item.availability, item.source)
            elif prior != (item.availability, item.source):
                raise AuditReconstructionError(
                    f"reused Version Identity {item.version_id} has inconsistent availability or source"
                )

        expected_complete = all(
            item.availability is EvidenceAvailability.AVAILABLE for item in self.evidence
        )
        if self.complete != expected_complete:
            raise AuditReconstructionError("reconstruction completeness must reflect evidence availability exactly")


@dataclass(frozen=True, slots=True)
class AuditReconstructionPackage:
    """Portable derived reference package; never an authoritative evidence replacement."""

    organization: OrganizationScope
    execution_subject_id: Identity
    evidence: tuple[tuple[str, Identity, EvidenceAvailability, str | None], ...]
    correlation_refs: tuple[Identity, ...]
    causation_refs: tuple[Identity, ...]
    complete: bool


def _manifest_evidence(manifest: ReconstructionManifest) -> tuple[tuple[str, GovernedVersionPin], ...]:
    items: list[tuple[str, GovernedVersionPin]] = [("workflow", manifest.workflow)]
    items.extend(("material-input", pin) for pin in manifest.material_inputs)
    if manifest.product_contract is not None:
        items.append(("product-contract", manifest.product_contract))
    items.extend(("gate-decision", pin) for pin in manifest.gate_decisions)
    items.extend(("execution-version", pin) for pin in manifest.execution_versions)
    items.extend(("result", pin) for pin in manifest.results)
    items.extend(("event", pin) for pin in manifest.events)
    return tuple(items)


def reconstruct_audit_view(
    *,
    manifest: ReconstructionManifest,
    organization: OrganizationScope,
    dispositions: tuple[EvidenceDisposition, ...] = (),
) -> AuditReconstructionView:
    """Build a derived audit view without inventing, replaying or mutating evidence.

    ``manifest`` is the exact-reference governed reconstruction produced by the
    RFC-0006 runtime. ``dispositions`` expresses current retention/redaction/
    availability state. Omitted dispositions mean available; duplicate, foreign,
    or unknown version dispositions fail closed.
    """

    if not isinstance(manifest, ReconstructionManifest):
        raise AuditReconstructionError("audit reconstruction requires a governed ReconstructionManifest")
    if not isinstance(organization, OrganizationScope) or organization != manifest.organization:
        raise AuditReconstructionError("audit reconstruction Organization context must exactly match evidence")
    if not isinstance(dispositions, tuple) or any(
        not isinstance(item, EvidenceDisposition) for item in dispositions
    ):
        raise AuditReconstructionError("evidence dispositions must be an immutable typed tuple")
    if len({item.version_id for item in dispositions}) != len(dispositions):
        raise AuditReconstructionError("one evidence Version Identity cannot have multiple dispositions")

    source_items = _manifest_evidence(manifest)

    # One version ID may occupy multiple semantic roles (e.g. material-input + result)
    # as long as every occurrence represents the exact same GovernedVersionPin.
    source_by_version: dict[Identity, tuple[str, GovernedVersionPin]] = {}
    for role, pin in source_items:
        prior = source_by_version.get(pin.version_id)
        if prior is None:
            source_by_version[pin.version_id] = (role, pin)
        elif prior[1] != pin:
            # Different pin semantics for the same Version Identity
            raise AuditReconstructionError(
                f"governed reconstruction contains ambiguous reused Version Identity: {pin.version_id}"
            )

    disposition_by_version = {item.version_id: item for item in dispositions}
    unknown = set(disposition_by_version) - set(source_by_version)
    if unknown:
        raise AuditReconstructionError("disposition references evidence outside the governed reconstruction")

    evidence: list[AuditEvidenceItem] = []
    for role, pin in source_items:
        disposition = disposition_by_version.get(pin.version_id)
        availability = (
            disposition.availability if disposition is not None else EvidenceAvailability.AVAILABLE
        )
        reason = disposition.reason if disposition is not None else None
        evidence.append(
            AuditEvidenceItem(
                role=role,
                availability=availability,
                source=pin if availability is EvidenceAvailability.AVAILABLE else None,
                version_id=pin.version_id,
                reason=reason,
            )
        )

    return AuditReconstructionView(
        organization=manifest.organization,
        execution_subject_id=manifest.execution_subject_id,
        initiating_actor_id=manifest.initiating_actor_id,
        operation_name=manifest.operation_name,
        evidence=tuple(evidence),
        correlation_refs=manifest.correlation_refs,
        causation_refs=manifest.causation_refs,
        complete=all(item.availability is EvidenceAvailability.AVAILABLE for item in evidence),
    )


def export_reconstruction_package(view: AuditReconstructionView) -> AuditReconstructionPackage:
    """Export portable exact references/status only; never hidden evidence content."""

    if not isinstance(view, AuditReconstructionView):
        raise AuditReconstructionError("reconstruction export requires an AuditReconstructionView")
    return AuditReconstructionPackage(
        organization=view.organization,
        execution_subject_id=view.execution_subject_id,
        evidence=tuple(
            (item.role, item.version_id, item.availability, item.reason) for item in view.evidence
        ),
        correlation_refs=view.correlation_refs,
        causation_refs=view.causation_refs,
        complete=view.complete,
    )
