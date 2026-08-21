# Arvectum OS Capability Catalog — Legacy Pointer

Status: `Deprecated / Informative`
Version: `0.8.0`
Updated: `2026-08-21`
Superseded by: [`docs/catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md`](../catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md)
Architecture basis: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)

## Purpose

This file is retained only as a historical navigation pointer for repository paths that previously referenced `docs/architecture/CAPABILITY-CATALOG.md`.

It is **not** the current lifecycle inventory and must not be used to infer whether a Platform Capability is `Candidate`, `Incubating`, `Active`, `Deprecated` or `Retired`.

The current governed capability lifecycle inventory is maintained in:

> [`docs/catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md`](../catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md)

That active catalog currently records the governed status of CAP-001 through CAP-004. This legacy-pointer update performs **no lifecycle transition** and grants no implementation, readiness, conformance, support or commercial status.

## Stable lifecycle semantics

Platform Capability lifecycle remains:

```text
Candidate → Incubating → Active → Deprecated → Retired
```

Platform Capability lifecycle is distinct from Product Contract lifecycle:

```text
Draft → Provisional → Stable → Deprecated → Retired
```

A roadmap milestone, successful product integration, experiment result or evidence package does not itself promote either lifecycle.

## Authority and conformance

Current lifecycle status must be read from the active governed catalog together with the applicable Constitution, Accepted RFC/ADR, approved decisions, Product Contracts and evidence.

This pointer is informative only. It does not create a public/stable platform contract, conformance claim, compatibility promise, operational-readiness statement, SLA/support commitment or commercial promise.

## Historical note

Earlier revisions of this file contained a pre-incubation capability inventory. That inventory became stale after the governed CAP-001 through CAP-004 incubation decisions and is intentionally no longer reproduced here. Repository history remains available for historical analysis.
