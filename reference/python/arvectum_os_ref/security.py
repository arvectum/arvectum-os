"""Organization and attributable-actor semantics for bounded reference tests."""

from __future__ import annotations

from dataclasses import dataclass

from .identity import Identity


@dataclass(frozen=True, slots=True)
class OrganizationScope:
    """Explicit organizational sovereignty scope with no ambient/default fallback."""

    organization_id: Identity

    def __post_init__(self) -> None:
        if not isinstance(self.organization_id, Identity):
            raise ValueError("organization_id must be an explicit Identity")


@dataclass(frozen=True, slots=True)
class Principal:
    """An attributable RFC-0002 Subject Identity participating as a principal.

    Mutable roles, permissions, lifecycle and other governed claims are
    intentionally excluded from this bounded step and do not live in Identity.
    """

    principal_id: Identity

    def __post_init__(self) -> None:
        if not isinstance(self.principal_id, Identity):
            raise ValueError("principal_id must be an Identity")


@dataclass(frozen=True, slots=True)
class ActorContext:
    """Principal acting in one explicit Organization scope.

    `represented_principal` preserves acting-on-behalf-of/impersonation context
    without erasing the actual actor. Authentication evidence is reference-only;
    it intentionally grants neither authorization nor Organizational Authority.
    """

    actual_principal: Principal
    organization: OrganizationScope
    represented_principal: Principal | None = None
    authentication_evidence_refs: tuple[Identity, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.actual_principal, Principal):
            raise ValueError("actual_principal must be explicit and attributable")
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("organization scope must be explicit")
        if self.represented_principal is not None and not isinstance(
            self.represented_principal, Principal
        ):
            raise ValueError("represented_principal must be a Principal when supplied")
        if not isinstance(self.authentication_evidence_refs, tuple) or any(
            not isinstance(ref, Identity) for ref in self.authentication_evidence_refs
        ):
            raise ValueError("authentication_evidence_refs must be Identity references")
