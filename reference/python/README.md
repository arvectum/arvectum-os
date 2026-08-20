# Arvectum OS Python Reference Harness

`reference/python/` is the executable reference and conformance harness used to exercise accepted Arvectum OS semantics, bounded Product Contract interactions and operational proofs.

It is **not** a product implementation, a public/stable SDK, a production-support promise, or an independent source of roadmap status.

## Canonical status and sequencing

Current phase, milestone, task status and next action are defined only by [`docs/roadmap/ROADMAP.md`](../../docs/roadmap/ROADMAP.md). This README intentionally does not repeat a current task number so that it cannot become a competing or stale roadmap.

Architecture and governance authority remain, in order, the Constitution, Accepted RFCs, Accepted ADRs, approved governance artifacts and Product Contracts. Reference code and tests implement and probe those decisions; they do not override them.

## What lives here

The harness is organized around a small number of implementation surfaces:

- `arvectum_os_ref/` — domain-neutral reference semantics for canonical records, identity, governed execution, event/provenance, Product Contracts/capability consumption, memory/knowledge and document/artifact governance;
- `bounded_product_ref/`, `p6_03_tender_operator_ref/`, `p6_07_discount_parser_ref/` and related fixtures — bounded product-side/reference adapters used to prove declared product/platform boundaries;
- `p6_*` scripts/modules — Phase 6 validation and migration/admission proofs retained as regression evidence;
- `p7_*` scripts/modules — persistent-runtime, durable-state, access, visibility, governed deploy/recovery, operational-contour, drill and portability proofs;
- `tests/` — the repository regression suite for the reference harness;
- `examples/` and semantic fixtures — executable or inspectable examples that support validation without becoming normative architecture.

Large proof modules are allowed when their responsibilities remain bounded, fail-closed and testable. File size alone is not a refactoring trigger; the approved Engineering Quality / Refactoring Gates decision requires refactoring when it is materially beneficial because of duplication, incohesion, hard-to-test coupling, dead paths or comparable maintainability defects.

## Operational and authority boundaries

Reference and operational-proof code must continue to preserve the accepted invariants, including:

- Authentication is not Authorization; Authorization is not Organizational Authority; technical access is not legal/organizational authority.
- Consequential canonical change proceeds through Governed Execution.
- Canonical Events are append-only; telemetry is non-canonical unless explicitly admitted.
- Observation is not validated Knowledge.
- Generated Artifact is Transient Output by default unless governed admission changes its state.
- Recovery/replay does not reissue historical external effects without a new authorization path.
- Product-specific workflows, schemas, knowledge, approval rules and UX remain product-owned unless a governed platform decision explicitly changes that boundary.
- External authoritative systems may remain authoritative; the harness must not create a competing source of truth.

## Validation

Run the complete local reference suite from this directory:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

Repository CI runs the same suite on Python 3.12 and rejects tracked Python bytecode/cache artifacts. See [`VALIDATION.md`](VALIDATION.md) for the durable validation procedure and scope.

## Generated files

Do not commit interpreter/runtime output such as `__pycache__/`, `*.pyc`, `*.pyo` or `.pytest_cache/`. The repository root `.gitignore` excludes these files and CI contains a regression guard that fails if they become tracked.

## Scope of claims

A passing reference suite demonstrates only the behavior covered by the current reference tests and recorded proof artifacts. It does not by itself establish Production readiness, lifecycle promotion, `Stable` Product Contracts, `Active` Platform Capabilities, broad host support, SLA/SLO/RPO/RTO commitments, certification, or full-platform conformance.
