# Python Reference Validation

This document defines the durable repository validation procedure for `reference/python/`. It replaces phase-specific command lists that can drift as the canonical roadmap advances.

## 1. Authority and scope

The validation procedure tests the executable reference harness against the repository state under review. It does not create or change architecture, Product Contract lifecycle, Platform Capability lifecycle, operational environment/readiness, conformance scope, support commitments or organizational authority.

Canonical sequencing and current status are defined only by [`docs/roadmap/ROADMAP.md`](../../docs/roadmap/ROADMAP.md).

## 2. Full local regression suite

From `reference/python/` run:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

The command must finish with `OK`. Focused test commands may be used while developing a bounded change, but they do not replace the full suite for milestone/code-health closure.

## 3. Repository hygiene check

From the repository root run:

```bash
tracked="$(git ls-files | grep -E '(^|/)__pycache__/|\.py[co]$|(^|/)\.pytest_cache/' || true)"
if [ -n "$tracked" ]; then
  printf '%s\n' "$tracked"
  exit 1
fi
```

Expected result: no tracked Python bytecode or cache artifacts.

The root `.gitignore` prevents normal reintroduction of these generated files, while CI independently checks the tracked tree so the guard is not dependent on local ignore behavior.

## 4. Canonical CI

`.github/workflows/reference-python-ci.yml` runs for pull requests that touch the reference harness, its workflow, or the repository Python-ignore rules, and can also be invoked manually with `workflow_dispatch`. CI:

1. checks out the exact repository revision;
2. installs Python 3.12;
3. rejects tracked generated Python bytecode/cache artifacts;
4. runs the complete unittest discovery suite in verbose mode.

A milestone Code Health Gate may cite the exact successful workflow run as evidence. CI success is necessary evidence for that gate when the reference harness changed, but it is not sufficient by itself: the required engineering-quality review must also assess duplication, cohesion, coupling/testability, dead/obsolete paths and other material maintainability risks.

## 5. Operational proofs

Selected-host, recovery, cross-host or external-system proofs may require owner-operated environments and evidence outside Git. Repository unit/integration tests do not silently substitute for those proofs. Conversely, owner-local proof evidence does not justify bypassing repository regression tests for code changes.

## 6. Claim boundary

Passing validation means the checked revision satisfies the executable checks above. It does not by itself mean external/customer Production readiness, broad portability, a stable/public API or persistence format, lifecycle promotion, certification, SLA/SLO/RPO/RTO support, or full-platform conformance.
