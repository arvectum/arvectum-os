# P9.07 product-owned Workspace contributions

This directory contains compile-time product UI contributions for the exact internal Productive Workspace release.

The platform-owned registry may select a contribution by opaque product contribution ID, but shared platform code must not absorb product schemas, workflows, approval rules, knowledge, templates or external-effect semantics from these components.

Current registered contributions:

- `tender-operator` — traceable to P6.02 Provisional 0.1.0;
- `discount-parser` — traceable to P6.06 Provisional 0.1.0.

This registry is internal and release-scoped. It is not a public/stable plugin API and does not create Product Contract or Platform Capability lifecycle promotion.
