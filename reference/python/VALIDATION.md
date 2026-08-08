# Reference Implementation Validation Cadence

Status: `Active`
Version: `1.0.0`
Created: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Canonical role: `subordinate engineering guidance`
Normative authority: `None beyond the Accepted sources and readiness baseline it references`

## Purpose

Keep executable validation useful and proportionate while the bounded Phase 1 reference implementation evolves.

This guidance does not create a Platform Capability, production-readiness claim, conformance claim, public support commitment or permanent CI/runtime architecture.

## Default full-suite command

```sh
cd reference/python
python -m unittest discover -s tests -v
```

## Validation cadence

1. After a substantial logical code block, run the smallest relevant targeted test set when practical.
2. Before marking any `P1.xx` implementation work item complete, run the full reference test suite once.
3. Before merge of a code-changing Phase 1 work item, obtain one successful full-suite CI run on the pull request.
4. Documentation-only changes do not require a Python test run unless they change executable commands, test expectations or CI behavior.
5. `P1.12` closure requires a final full-suite run plus review of the Phase 1 architecture-fitness evidence matrix.

A practical targeted pattern is:

```sh
cd reference/python
python -m unittest discover -s tests -p 'test_p1_08*.py' -v
```

Use the test module or pattern for the changed work item and directly affected dependencies. Do not run unrelated suites merely to create activity.

## Failure handling

Do not use blind retry as a substitute for diagnosis.

When a test fails:

1. identify whether the failure is caused by the implementation, the test, the fixture or nondeterminism;
2. correct the cause;
3. rerun the failed or directly affected tests;
4. after they pass, run the full suite once before declaring the work item complete or merge-ready.

A test that changes outcome without a relevant code or fixture change is defect evidence and should be treated as flakiness rather than retried until green.

## CI boundary

The repository CI workflow is intentionally minimal:

- one Python job;
- one full `unittest` suite;
- no version matrix;
- no coverage gate;
- no lint/security/tooling bundle added by default;
- pull-request execution only when `reference/python/**` or the CI workflow itself changes;
- manual `workflow_dispatch` for an explicit stage-end validation run;
- concurrent superseded runs are cancelled.

The normal working convention is to open the pull request when the logical implementation block is ready for validation. Additional CI runs should normally occur only when a failed or changed implementation requires another validation pass.

## Evidence meaning

A passing test or CI run is implementation and architecture-fitness evidence within the bounded reference scope. It does not by itself:

- make a capability `Active`;
- establish operational readiness;
- establish production status;
- authorize a full-platform conformance claim;
- select GitHub Actions or Python as permanent platform architecture.

## Architecture boundary

This cadence is a reversible engineering practice consistent with Constitution `1.2.0`, Accepted RFC-0001 and `docs/implementation/REFERENCE-IMPLEMENTATION-READINESS.md`.

No ADR is required for this bounded CI usage. If build/validation infrastructure later becomes a durable cross-product dependency, customer-facing control, material evidence-integrity mechanism or otherwise crosses an ADR trigger in the readiness baseline, reassess it at that time using the lowest sufficient governance artifact.
