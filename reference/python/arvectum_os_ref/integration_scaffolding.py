"""P5.05 — internal/provisional scaffolding and local integration harness.

This module reduces repeated setup around the P5.04 integration composition
facade without creating a Stable/public SDK, generated-code compatibility
contract, package boundary, serialization format, registry, network service or
production-infrastructure dependency.

Templates deliberately expose a tiny, understandable product-owned entry module
that imports Arvectum OS only through ``integration_composition``. The local
harness composes the exact Product Contract/dependency evidence through the
P5.04 facade and provides bounded smoke checks only; it grants no Authorization,
Organizational Authority, approval, data right or capability lifecycle state.
"""

from __future__ import annotations

from dataclasses import dataclass

from .execution import GovernedVersionPin
from .integration_composition import IntegrationCompositionFacade, compose_integration_facade
from .product_contract import ProductContract
from .product_contract_resolution import GovernedDependencyVersionEvidence
from .security import ActorContext
from .workspace_shell import PresentationAuthority, WorkspaceShellState


@dataclass(frozen=True, slots=True)
class IntegrationTemplate:
    """Rendered, replaceable starter artifact for one bounded integration."""

    module_name: str
    source: str
    provisional: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.module_name, str) or not self.module_name.isidentifier():
            raise ValueError("template module_name must be a valid Python identifier")
        if not isinstance(self.source, str) or not self.source.strip():
            raise ValueError("template source must be explicit")
        if self.provisional is not True:
            raise ValueError("P5.05 generated/template artifacts must remain provisional")


def render_integration_entry_template(*, module_name: str = "integration_entry") -> IntegrationTemplate:
    """Render the smallest understandable product-owned facade entry template.

    The template intentionally contains no Product Contract construction,
    dependency resolver logic, authorization logic, domain semantics or
    production configuration. Those remain with their existing semantic owners
    or the consuming product.
    """

    if not isinstance(module_name, str) or not module_name.isidentifier():
        raise ValueError("template module_name must be a valid Python identifier")

    source = '''"""Internal/provisional Arvectum OS integration entry.

Replace or extend this product-owned module as the integration evolves. The
current Python import shape is reference evidence, not a Stable/public SDK
compatibility promise.
"""

from arvectum_os_ref.integration_composition import IntegrationCompositionFacade


def open_integration_workspace(*, facade: IntegrationCompositionFacade):
    """Enter the non-authoritative workspace through the composed facade."""

    return facade.open_workspace()
'''
    return IntegrationTemplate(module_name=module_name, source=source)


@dataclass(frozen=True, slots=True)
class LocalIntegrationHarnessResult:
    """Bounded local smoke evidence; never an authority or readiness decision."""

    facade: IntegrationCompositionFacade
    workspace: WorkspaceShellState
    product_contract: GovernedVersionPin
    provisional: bool = True

    def __post_init__(self) -> None:
        if self.provisional is not True:
            raise ValueError("P5.05 local harness evidence must remain provisional")
        if self.workspace.presentation_authority is not PresentationAuthority.NON_AUTHORITATIVE:
            raise ValueError("local harness workspace must remain non-authoritative")
        if self.facade.context.product_contract != self.product_contract:
            raise ValueError("local harness lost exact Product Contract Version continuity")
        if (
            self.workspace.product_context is None
            or self.workspace.product_context.product_contract_version_id
            != self.product_contract.version_id
        ):
            raise ValueError("local harness workspace lost exact Product Contract Version continuity")


def run_local_integration_harness(
    *,
    contract: ProductContract,
    actor: ActorContext,
    effective_product_contract: GovernedVersionPin,
    governed_versions: tuple[GovernedDependencyVersionEvidence, ...],
) -> LocalIntegrationHarnessResult:
    """Compose and smoke-check a bounded integration without production services.

    All declaration/compatibility checks are delegated to P5.04 composition,
    which itself delegates to the P5.02/P5.03 semantic owners. No database,
    broker, network endpoint, package registry, IAM provider or deployment
    topology is required or implied by this local harness.
    """

    facade = compose_integration_facade(
        contract=contract,
        actor=actor,
        effective_product_contract=effective_product_contract,
        governed_versions=governed_versions,
    )
    workspace = facade.open_workspace()
    return LocalIntegrationHarnessResult(
        facade=facade,
        workspace=workspace,
        product_contract=contract.version_pin,
    )
