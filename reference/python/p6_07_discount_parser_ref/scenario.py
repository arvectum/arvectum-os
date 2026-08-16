"""Synthetic/offline P6.07 controlled-publication integration proof.

No real Telegram network call, customer data, bot token or reusable secret exists
in this fixture. Product-owned Discount Parser objects cross the boundary only as
stable minimized references. The only shared capability consumed is CAP-004.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

from arvectum_os_ref.audit_reconstruction_support import AuditReconstructionView
from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.event_provenance import ReconstructionManifest
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.integration_adapters import IntegrationAdapters, compose_integration_adapters
from arvectum_os_ref.product_capability_consumption import (
    CAP_004_AUDIT_RECONSTRUCTION,
    CAPABILITY_CONTRACT_VERSION,
    OP_RECONSTRUCT_EXECUTION,
    CapabilityConsumptionRequest,
)
from arvectum_os_ref.product_contract_resolution import (
    DependencySupportDisposition,
    GovernedDependencyVersionEvidence,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal

from .contract import PRODUCT_COMPATIBILITY_LINE, build_p6_06_product_contract_projection
from .journey import reconstruct_publication


UTC = timezone.utc
PURPOSE = "controlled-publication-reconstruction"
CLASSIFICATION = "internal"


class PublicationOutcome(str, Enum):
    PUBLISHED = "published"
    FAILED = "failed"
    DUPLICATE_NOT_APPLICABLE = "duplicate/not-applicable"
    UNCERTAIN_RECONCILIATION_REQUIRED = "uncertain/reconciliation-required"


class P607Stage1Error(RuntimeError):
    """Synthetic Stage 1 safety boundary rejected the publication attempt."""


@dataclass(frozen=True, slots=True)
class ProductBoundaryReferences:
    """Minimized product-owned references; these are not platform domain schemas."""

    parse_run: GovernedVersionPin
    source_observation: GovernedVersionPin
    offer: GovernedVersionPin
    publication_candidate: GovernedVersionPin
    rule_config: GovernedVersionPin
    template_version: GovernedVersionPin
    publication_reservation: GovernedVersionPin
    publication_attempt: GovernedVersionPin
    telegram_target: GovernedVersionPin


@dataclass(frozen=True, slots=True)
class FakeTelegramResult:
    outcome: PublicationOutcome
    telegram_message: GovernedVersionPin | None = None


class FakeTelegramAdapter:
    """Product-owned fake external adapter used only for Stage 1 safety proof."""

    def __init__(self, planned_outcome: PublicationOutcome = PublicationOutcome.PUBLISHED) -> None:
        if not isinstance(planned_outcome, PublicationOutcome):
            raise ValueError("planned_outcome must be explicit")
        self.planned_outcome = planned_outcome
        self.send_calls = 0

    def publish(
        self,
        *,
        candidate: GovernedVersionPin,
        target: GovernedVersionPin,
    ) -> FakeTelegramResult:
        if not isinstance(candidate, GovernedVersionPin) or not isinstance(target, GovernedVersionPin):
            raise TypeError("fake Telegram publication requires exact product boundary references")
        if candidate.subject_id.scope != target.subject_id.scope:
            raise P607Stage1Error("candidate and Telegram target must share Organization scope")

        self.send_calls += 1
        if self.planned_outcome is PublicationOutcome.PUBLISHED:
            scope = candidate.subject_id.scope
            return FakeTelegramResult(
                outcome=self.planned_outcome,
                telegram_message=_pin(
                    "telegram-message",
                    "synthetic-message-4242",
                    "discount-parser.telegram-message-ref",
                    scope,
                    authority_scope="external-reference/telegram-message",
                    lifecycle_status="Observed",
                ),
            )
        return FakeTelegramResult(outcome=self.planned_outcome)


@dataclass(frozen=True, slots=True)
class Stage1Scenario:
    organization: OrganizationScope
    actor: ActorContext
    contract: object
    adapters: IntegrationAdapters
    governed_versions: tuple[GovernedDependencyVersionEvidence, ...]
    reconstruction_request: CapabilityConsumptionRequest
    refs: ProductBoundaryReferences


@dataclass(frozen=True, slots=True)
class Stage1ExecutionResult:
    outcome: PublicationOutcome
    telegram_message: GovernedVersionPin | None
    telegram_send_calls: int
    manifest: ReconstructionManifest
    reconstruction: AuditReconstructionView


def _id(namespace: str, value: str, scope: str) -> Identity:
    return Identity(namespace, value, scope)


def _pin(
    role: str,
    value: str,
    semantic_type: str,
    scope: str,
    *,
    authority_scope: str | None = None,
    lifecycle_status: str = "Retained",
) -> GovernedVersionPin:
    return GovernedVersionPin(
        _id(f"{role}-subject", value, scope),
        _id(f"{role}-version", f"{value}-v1", scope),
        semantic_type,
        authority_scope or f"{semantic_type}/reference",
        lifecycle_status,
    )


def _product_refs(scope: str) -> ProductBoundaryReferences:
    return ProductBoundaryReferences(
        parse_run=_pin("parse-run", "run-001", "discount-parser.parse-run-ref", scope),
        source_observation=_pin(
            "source-observation",
            "source-observation-001",
            "discount-parser.source-observation-ref",
            scope,
            authority_scope="external-reference/source-observation",
        ),
        offer=_pin("offer", "offer-001", "discount-parser.offer-ref", scope),
        publication_candidate=_pin(
            "publication-candidate",
            "candidate-001",
            "discount-parser.publication-candidate-ref",
            scope,
        ),
        rule_config=_pin("rule-config", "rules-001", "discount-parser.rule-config-ref", scope),
        template_version=_pin(
            "template-version",
            "template-001",
            "discount-parser.template-version-ref",
            scope,
        ),
        publication_reservation=_pin(
            "publication-reservation",
            "reservation-001",
            "discount-parser.publication-attempt-ref",
            scope,
            lifecycle_status="ReservedBeforeEffect",
        ),
        publication_attempt=_pin(
            "publication-attempt",
            "attempt-001",
            "discount-parser.publication-attempt-ref",
            scope,
            lifecycle_status="IntentRecorded",
        ),
        telegram_target=_pin(
            "telegram-target",
            "synthetic-channel",
            "discount-parser.telegram-message-ref",
            scope,
            authority_scope="external-reference/telegram-channel",
            lifecycle_status="Referenced",
        ),
    )


def build_stage1_scenario(*, scope: str = "p6-07-org-a") -> Stage1Scenario:
    organization = OrganizationScope(Identity("organization", scope, "platform"))
    actor = ActorContext(
        Principal(Identity("principal", "p6-07-publication-operator", scope)),
        organization,
    )
    created_at = datetime(2026, 8, 16, 14, 30, tzinfo=UTC)
    contract = build_p6_06_product_contract_projection(actor=actor, created_at=created_at)

    governance_reference = "docs/contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md@1.0.0"
    governed_versions = (
        GovernedDependencyVersionEvidence(
            CAP_004_AUDIT_RECONSTRUCTION,
            CAPABILITY_CONTRACT_VERSION,
            DependencySupportDisposition.SUPPORTED,
            governance_reference,
        ),
    )
    adapters = compose_integration_adapters(
        contract=contract,
        actor=actor,
        effective_product_contract=contract.version_pin,
        governed_versions=governed_versions,
    )
    access = AccessRequest(actor, PURPOSE, "read", (CLASSIFICATION,))
    reconstruction_request = CapabilityConsumptionRequest(
        organization=organization,
        product_id=contract.product_id,
        product_version=PRODUCT_COMPATIBILITY_LINE,
        dependency_id=CAP_004_AUDIT_RECONSTRUCTION,
        dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
        operation_name=OP_RECONSTRUCT_EXECUTION,
        access=access,
    )

    return Stage1Scenario(
        organization=organization,
        actor=actor,
        contract=contract,
        adapters=adapters,
        governed_versions=governed_versions,
        reconstruction_request=reconstruction_request,
        refs=_product_refs(scope),
    )


def _manifest_for_outcome(
    scenario: Stage1Scenario,
    *,
    outcome: PublicationOutcome,
    telegram_message: GovernedVersionPin | None,
) -> tuple[ReconstructionManifest, tuple[tuple[Identity, str, tuple[str, ...], str], ...]]:
    scope = scenario.organization.organization_id.value
    refs = scenario.refs
    workflow = _pin(
        "workflow",
        "controlled-telegram-publication-v1",
        "discount-parser.controlled-publication-workflow-ref",
        scope,
    )
    approval = _pin(
        "gate-decision",
        "synthetic-manual-operator-approval",
        "platform.governed-gate-decision",
        scope,
        lifecycle_status="Satisfied",
    )
    execution = _pin(
        "execution",
        "p6-07-stage1-publication",
        "platform.execution-context",
        scope,
        lifecycle_status="Completed",
    )
    outcome_result = _pin(
        "publication-outcome",
        outcome.value.replace("/", "-"),
        "discount-parser.publication-outcome-ref",
        scope,
        lifecycle_status="Observed",
    )
    event = _pin(
        "event",
        f"publication-{outcome.value.replace('/', '-')}",
        "platform.event",
        scope,
        lifecycle_status="Admitted",
    )

    material_inputs = (
        refs.parse_run,
        refs.source_observation,
        refs.offer,
        refs.publication_candidate,
        refs.rule_config,
        refs.template_version,
        refs.publication_reservation,
        refs.publication_attempt,
        refs.telegram_target,
    )
    results = (outcome_result,) + ((telegram_message,) if telegram_message is not None else ())
    pins = (
        workflow,
        *material_inputs,
        scenario.contract.version_pin,
        approval,
        execution,
        *results,
        event,
    )
    provenance_refs = tuple(
        dict.fromkeys(
            (
                scenario.actor.actual_principal.principal_id,
                execution.subject_id,
                *(identity for pin in pins for identity in (pin.subject_id, pin.version_id)),
            )
        )
    )
    manifest = ReconstructionManifest(
        organization=scenario.organization,
        execution_subject_id=execution.subject_id,
        initiating_actor_id=scenario.actor.actual_principal.principal_id,
        operation_name="discount-parser.controlled-telegram-publication",
        workflow=workflow,
        material_inputs=material_inputs,
        product_contract=scenario.contract.version_pin,
        gate_decisions=(approval,),
        execution_versions=(execution,),
        results=results,
        events=(event,),
        event_types=(("discount-parser.publication-outcome-observed", "1"),),
        correlation_refs=(execution.subject_id, refs.publication_attempt.subject_id),
        causation_refs=(refs.publication_reservation.version_id, refs.publication_attempt.version_id),
        provenance_refs=provenance_refs,
    )
    constraints = tuple(
        (pin.version_id, PURPOSE, ("read",), CLASSIFICATION)
        for pin in pins
    )
    return manifest, constraints


def execute_stage1_publication(
    scenario: Stage1Scenario,
    *,
    telegram: FakeTelegramAdapter,
    pre_effect_evidence_available: bool = True,
    duplicate_reserved: bool = False,
) -> Stage1ExecutionResult:
    """Execute one bounded offline publication simulation then reconstruct it.

    Safety behavior deliberately precedes the fake external call: missing required
    intent/reservation evidence fails closed; a known duplicate is not sent; an
    ambiguous external outcome is recorded as reconciliation-required and is not
    retried automatically.
    """

    if not isinstance(scenario, Stage1Scenario):
        raise TypeError("scenario must be Stage1Scenario")
    if not isinstance(telegram, FakeTelegramAdapter):
        raise TypeError("Stage 1 requires the explicit fake Telegram adapter")
    if scenario.adapters.facade.context.product_contract != scenario.contract.version_pin:
        raise P607Stage1Error("composed integration lost exact Product Contract continuity")

    if not pre_effect_evidence_available:
        raise P607Stage1Error("required pre-effect intent/reservation evidence is unavailable")

    if duplicate_reserved:
        outcome = PublicationOutcome.DUPLICATE_NOT_APPLICABLE
        telegram_message = None
    else:
        external = telegram.publish(
            candidate=scenario.refs.publication_candidate,
            target=scenario.refs.telegram_target,
        )
        outcome = external.outcome
        telegram_message = external.telegram_message

    manifest, constraints = _manifest_for_outcome(
        scenario,
        outcome=outcome,
        telegram_message=telegram_message,
    )
    reconstruction = reconstruct_publication(
        adapters=scenario.adapters,
        request=scenario.reconstruction_request,
        governed_versions=scenario.governed_versions,
        manifest=manifest,
        evidence_constraints=constraints,
    )
    return Stage1ExecutionResult(
        outcome=outcome,
        telegram_message=telegram_message,
        telegram_send_calls=telegram.send_calls,
        manifest=manifest,
        reconstruction=reconstruction,
    )
