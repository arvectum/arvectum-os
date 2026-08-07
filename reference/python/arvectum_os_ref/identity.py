"""Kernel identity value semantics for the first bounded executable slice."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Identity:
    """Opaque, stable and immutable reference within a declared namespace/scope.

    The value deliberately carries no permission, authority, role or mutable
    business meaning. Wire encoding is not a stable public contract here.
    """

    namespace: str
    value: str
    scope: str

    def __post_init__(self) -> None:
        for field_name in ("namespace", "value", "scope"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
