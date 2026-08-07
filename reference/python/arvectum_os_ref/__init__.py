"""Bounded Arvectum OS reference implementation harness.

This package is intentionally provisional and is not a public platform contract.
"""

from .canonical import AuthorityMode, CanonicalRecord, build_p1_02_native_record
from .identity import Identity
from .security import ActorContext, OrganizationScope, Principal

__all__ = [
    "ActorContext",
    "AuthorityMode",
    "CanonicalRecord",
    "Identity",
    "OrganizationScope",
    "Principal",
    "build_p1_02_native_record",
]
