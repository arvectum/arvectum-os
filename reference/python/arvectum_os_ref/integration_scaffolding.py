"""P5.05/R15 — internal/provisional scaffolding and local integration harness.

P5.05 reduced repeated setup around the composition facade. After P5.08/P5.09
proved a materially reused adapter seam, R15 aligns the default developer path
with that demonstrated boundary instead of continuing to teach new consumers the
lower-level facade directly.

The scaffold remains readable and replaceable. Workspace presentation is an
explicit optional binding over the shared capability-first adapter core; the
harness creates no Stable/public SDK, generated-code compatibility contract,
package boundary, serialization format, registry, network service or production
infrastructure dependency.
"""

from __future__ import annotations

from dataclasses import dataclass

from .execution import GovernedVersionPin
from .integration_adapters import (
    IntegrationAdapters,
    compose_integration_adapters,
    compose_workspace_adapter,
)
from .integration_composition import IntegrationCompositionFacade
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
            raise ValueError("P5.05/R15 generated/template artifacts must remain provisional")


def render_integration_entry_template(*, module_name: str = "integration_entry") -> IntegrationTemplate:
    """Render the smallest understandable product-owned adapter entry template.

    The template intentionally contains no Product Contract construction,
    dependency resolver logic, authorization logic, domain semantics or
    production configuration. It receives an already composed IntegrationAdapters
    value and opts into workspace presentation only when the product needs it.
    """

    if not isinstance(module_name, str) or not module_name.isidentifier():
        raise ValueError("template module_name must be a valid Python identifier")

    source = '''"""Internal/provisional Arvectum OS integration entry.

Replace or extend this product-owned module as the integration evolves. The
current Python import shape is reference evidence, not a Stable/public SDK
compatibility promise.
"""

from arvectum_os_ref.integration_adapters import IntegrationAdapters, compose_workspace_adapter


def open_integration_workspace(*, adapters: IntegrationAdapters):
    """Opt into non-authoritative workspace presentation for this consumer."""

    return compose_workspace_adapter(adapters=adapters).open()
'''
    return IntegrationTemplate(module_name=module_name, source=source)


@dataclass(frozen=True, slots=True)
class LocalIntegrationHarnessResult:
    """Bounded local smoke evidence; never an authority or readiness decision."""

    adapters: IntegrationAdapters
    workspace: WorkspaceShellState
    product_contract: GovernedVersionPin
    provisional: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.adapters, IntegrationAdapters):
            raise ValueError("local harness requires the shared IntegrationAdapters core")
        if self.provisional is not True:
            raise ValueError("P5.05/R15 local harness evidence must remain provisional")
        if self.workspace.presentation_authority is not PresentationAuthority.NON_AUTHORITATIVE:
            raise ValueError("local harness workspace must remain non-authoritative")
        if self.adapters.facade.context.product_contract != self.product_contract:
            raise ValueError("local harness lost exact Product Contract Version continuity")
        if (
            self.workspace.product_context is None
            or self.workspace.product_context.product_contract_version_id
            != self.product_contract.version_id
        ):
            raise ValueError("local harness workspace lost exact Product Contract Version continuity")

    @property
    def facade(self) -> IntegrationCompositionFacade:
        """Internal compatibility convenience; the reusable harness state is adapters."""

        return self.adapters.facade


def run_local_integration_harness(
    *,
    contract: ProductContract,
    actor: ActorContext,
    effective_product_contract: GovernedVersionPin,
    governed_versions: tuple[GovernedDependencyVersionEvidence, ...],
) -> LocalIntegrationHarnessResult:
    """Compose and smoke-check a bounded integration without production services.

    Declaration/compatibility checks are delegated through the same adapter
    composition used by both demonstrated consumers. Workspace is then bound
    explicitly for this workspace-oriented local smoke. No database, broker,
    network endpoint, package registry, IAM provider or deployment topology is
    required or implied by this local harness.
    """

    adapters = compose_integration_adapters(
        contract=contract,
        actor=actor,
        effective_product_contract=effective_product_contract,
        governed_versions=governed_versions,
    )
    workspace = compose_workspace_adapter(adapters=adapters).open()
    return LocalIntegrationHarnessResult(
        adapters=adapters,
        workspace=workspace,
        product_contract=contract.version_pin,
    )
