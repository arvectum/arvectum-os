# P4.10 — Hosted CI Validation Evidence

Status: `Complete`
Date: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Related work item: `P4.10 — Workspace architecture fitness + accessibility/usability baseline`
Result: **`PASS — hosted runner provisioning is restored and the current P4.10 reference state passes the full Reference Python CI suite.`**

## Purpose

This record closes the execution-evidence gap left when GitHub-hosted runners stopped provisioning during P4.08–P4.10.

It is engineering evidence only. It does not create or modify architecture, Product Contracts, capability lifecycle, conformance scope, production readiness or accessibility certification.

## Runner recovery signal

The previously failed `Reference Python CI #189` job from PR #56 was re-run on `2026-08-09` after issue #54 had remained open with zero-step provisioning failures.

The re-run reached checkout, Python setup and test execution successfully and completed with:

- runner image: Ubuntu `24.04.4` / `ubuntu-24.04`;
- Python: CPython `3.12.13`;
- command: `python -m unittest discover -s tests -v`;
- result: `551 tests`, `OK`.

That re-run proved hosted runner provisioning was functioning again, but validated the older PR #56 merge ref rather than the completed P4.10 repository state.

## Current P4.10 validation

PR #57 was created from `main` after P4.10 completion and canonical synchronization. It adds this validation record plus one additional P4.10 positive-path regression proving that a unique current allow decision remains explicit, minimized and non-authoritative.

`Reference Python CI #190` then executed successfully on the PR #57 merge ref containing the completed P4.10 state and the added regression:

- workflow: `Reference Python CI`;
- run number: `#190`;
- job: `Full reference test suite`;
- runner image: Ubuntu `24.04.4` / `ubuntu-24.04`;
- Python: CPython `3.12.13`;
- command: `python -m unittest discover -s tests -v`;
- result: **`559 tests`, `OK`**.

The observed log includes successful execution of all P4.10 tests, including:

- the 14-dimension fitness inventory guard;
- accessibility/textual-semantic baseline guard;
- operator object/version/authority/action/reason comprehension guard;
- deterministic fail-closed visibility states;
- Product Contract and R10/Governed Execution choke-point continuity;
- narrow source-authorization helper reuse boundary;
- presentation reversibility / technology-neutrality;
- the additional positive-path authority-safe decision-consumption regression.

## Issue #54 disposition

The issue #54 done conditions are now satisfied by observed GitHub Actions evidence:

1. a normal hosted `Reference Python CI` run reaches checkout, Python setup and test steps;
2. `python -m unittest discover -s tests -v` executes on the current P4.10-based PR state;
3. Python version and test result are visible in Actions logs;
4. no architecture, security, authority or governance exception was required to restore execution.

Issue #54 may therefore be closed as completed.

## Architecture / governance disposition

This validation changes no P4.10 architecture result:

- Constitution `1.2.0` remains unchanged;
- RFC-0001 through RFC-0008 remain `Accepted 1.0.0`;
- no ADR is introduced;
- P4.08 Product Contract remains `Provisional 0.1.0`;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- the P4.10 accessibility baseline remains bounded semantic/textual evidence, not formal WCAG or production certification;
- the current canonical action remains `R12 — M4 Workspace Hardening`.
