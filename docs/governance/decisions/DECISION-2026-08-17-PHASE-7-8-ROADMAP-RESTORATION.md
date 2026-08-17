# DECISION-2026-08-17 — Restore Phase 7/8 strategic roadmap and activate Phase 7

Status: `Approved`
Date: `2026-08-17`
Decision owner: `ООО «Арвектум»`
Task classification: `governance` with `platform`
Scope: canonical roadmap sequencing after M6
Constitution: `1.2.0`
Architecture baseline: RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)
Related roadmap: `docs/roadmap/ROADMAP.md`
Predecessor milestone: `M6 — Product-driven platform validation`, achieved

## 1. Context

The historical canonical roadmap explicitly retained two strategic phases after Phase 6:

- `Phase 7 — Operational / Enterprise Readiness`, milestone `M7 — Scoped production-grade operating baseline`;
- `Phase 8 — Ecosystem and External Integration`, milestone `M8 — Governed external ecosystem baseline`.

A later simplification of the master roadmap removed those future rows while Phase 6 execution was being tracked in detail. No separate canonical decision retired Phase 7 or Phase 8.

Phase 6 / M6 is now complete with two materially distinct real-product validation chains, real governed evidence, a passing M6 Milestone Code Health Gate, and no lifecycle or public-contract promotion. The current master roadmap otherwise has no next governed action.

The owner has directed that the missing strategic continuation be restored and decomposed into executable work.

## 2. Decision

### 2.1 Restore the strategic continuation

The canonical roadmap SHALL again include:

1. `Phase 7 — Operational / Enterprise Readiness`;
2. `Phase 8 — Ecosystem and External Integration`.

The restored names and milestone intents preserve the historical canonical direction. Their detailed work breakdown is revalidated against the actual M6 evidence rather than copied mechanically from an earlier planning hypothesis.

### 2.2 Activate Phase 7

Phase 7 becomes `Active` because:

- M6 is achieved;
- two real product/workflow contours have exercised the platform boundary;
- owner-operated Mac mini execution is already proven in bounded real use;
- the main remaining platform question is no longer whether real product reuse works, but whether the platform can operate persistently, recoverably, securely and observably as an internal organizational foundation.

Phase 7 does not require a Platform Capability to become `Active` merely to begin internal persistent operation.

### 2.3 Persistent Mac mini operation is an early Phase 7 objective

Phase 7 SHALL not postpone regular Arvectum OS use until the entire enterprise-readiness phase is complete.

The sequence is:

- `P7.01` defines the persistent internal operating boundary and exact readiness requirements;
- `P7.02` establishes a supervised persistent owner-operated Arvectum OS runtime on the selected Mac mini with boot/restart lifecycle, safe configuration/secrets separation, health evidence and rollback/removal path.

After `P7.02` passes its declared gates, Arvectum OS MAY enter **regular persistent internal operation** on that Mac mini for ООО «Арвектум» while later Phase 7 work hardens durability, backup/recovery, observability, upgrades, incident handling and portability.

This operational classification is `Persistent Internal / owner-operated`. It is not by itself:

- an external/customer `Production` environment claim;
- an `Active` Platform Capability transition;
- a `Stable` Product Contract;
- an SLA/support commitment;
- a stable public deployment topology;
- a supported macOS platform promise.

The Mac mini remains the current operational environment, not the architecture contract.

### 2.4 Phase 8 remains Draft

Phase 8 is restored as a `Draft / Exploratory` strategic phase. It SHALL not become active before M7 closure and a fresh boundary revalidation against actual operational evidence, external integration needs, organization-isolation requirements, rights, portability and commercial commitments.

Phase 8 planning creates no public API, partner program, customer deployment promise or multi-tenant production commitment.

### 2.5 Engineering quality gates

The Approved `DECISION-2026-08-08 — Engineering Quality and Refactoring Gates` remains binding.

Phase 7 uses explicit R21–R24 checkpoints and MUST include a pre-closure M7 Milestone Code Health Gate. Phase 8 planning defines provisional R25–R28 checkpoints, subject to revalidation at activation.

## 3. Compatibility

This decision is compatible with Constitution `1.2.0` and Accepted RFC-0001 through RFC-0008 because it:

- preserves domain-neutral platform responsibility;
- keeps product-specific workflows product-owned;
- preserves Product Contract boundaries;
- keeps authentication, authorization, Organizational Authority and data governance distinct;
- treats operational telemetry as non-canonical by default;
- preserves external authority and portability;
- does not silently promote observations into Knowledge or operational policy;
- does not select a permanent technology topology through roadmap text alone.

No Accepted RFC or Constitution amendment is required to restore these roadmap phases.

## 4. Consequences

Positive consequences:

- roadmap continuity is restored instead of stopping artificially at M6;
- permanent internal use begins early enough to generate real operational evidence;
- enterprise-readiness work is driven by a live internal system rather than a hypothetical deployment;
- customer/external ecosystem commitments remain deferred until the platform has a demonstrated persistent operating baseline.

Trade-offs:

- Phase 7 will expose operational debt that bounded validation intentionally tolerated;
- persistent operation may force concrete storage, service-management, backup, IAM or deployment choices across ADR/stable-boundary gates;
- some capabilities and Product Contracts may intentionally remain Incubating/Provisional through M7 if lifecycle promotion is not justified.

## 5. Canonical follow-up

This decision is implemented by:

- `docs/roadmap/PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md`;
- `docs/roadmap/PHASE-8-ECOSYSTEM-EXTERNAL-INTEGRATION.md`;
- synchronization of `docs/roadmap/ROADMAP.md`.

The current next action after publication is `P7.01 — Persistent internal operating boundary + operational requirements baseline`.
