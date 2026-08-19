# P7.07 — Selected-Mac Attempt 1 product-bridge loader blocker

Date: `2026-08-19`
Status: `Repository remediation prepared; selected-Mac re-proof pending`
Task classification: `platform` with `product_contract`
Constitution: `1.2.0 Ratified`
Product Contract: P6.02 `Provisional 0.1.0`

## 1. Scope

This record preserves the first selected-Mac closure attempt for `P7.07 — Persistent Tender Operator operational contour` and the bounded repository remediation required before the proof may continue.

It does not close P7.07, change its Product Contract, alter EIS authority, promote any lifecycle, or authorize P7.08.

## 2. Attempt result

Selected-Mac Steps 1–6 passed on exact canonical/runtime release:

`bf1a3047aadf03384c9525eacd4e186a53092c11`

The guarded one-time setup returned:

`PASS_ADMITTED_AND_CONFIGURED`

The resulting exact P7.07 governed item remained present with its exact item-scoped P7.04 read authorization. The temporary setup grant was revoked successfully.

The first guarded product consumption in Step 7 failed closed before any supervised restart:

`RESULT=BLOCKED error=AttributeError:'NoneType' object has no attribute '__dict__'`

## 3. Root cause

The private P7.07 dynamic loader created the product-owned bridge module with `importlib.util.module_from_spec(...)` and called `spec.loader.exec_module(module)` without first registering the module under its exact `module_name` in `sys.modules`.

The canonical `arvectum/tender-agent` bridge is a `@dataclass(frozen=True, slots=True)`. Python `dataclasses` resolves annotation/module context through `sys.modules[cls.__module__]` while processing this class shape. Because the private dynamic loader had not registered the module, class construction failed before CAP-001 consumption.

The defect was reproduced on the selected Mac under both available Python 3.14.7 and Python 3.11 interpreters. It is therefore classified as a repository loader defect, not product-checkout drift or selected-host interpreter drift.

## 4. Fail-closed disposition

No workaround was permitted or used.

In particular, the operator did not:

- modify the immutable active release;
- modify the canonical clean product checkout;
- remove `slots=True` from the product bridge;
- replace the interpreter merely to bypass the failed proof;
- trigger the supervised restart after the pre-restart product consumption had failed.

Post-failure checks confirmed:

- P7.03 integrity remained `PASS`;
- the persistent runtime remained on the same pre-proof instance/generation because restart did not occur;
- active temporary P7.07 setup grants remained zero;
- the exact persistent item-scoped read grant remained effective;
- the canonical platform and product checkouts remained clean;
- no new EIS/SOAP retrieval or product/external effect occurred.

## 5. Bounded repository remediation

The remediation is deliberately implementation-local:

1. import `sys` in `p7_07_persistent_tender_operator_contour.py`;
2. register the module as `sys.modules[module_name] = module` immediately before `spec.loader.exec_module(module)`;
3. add focused regression coverage that executes the real dynamic loader against a temporary `@dataclass(frozen=True, slots=True)` product bridge rather than mocking `_load_product_bridge` or `run_consume`.

This changes no P7.03 persistence semantics, P7.04 authorization semantics, Product Contract declaration, EIS authority mapping, CAP-001 contract, Governed Execution semantics or product-owned procurement behavior.

## 6. Functional review

### Product / platform boundary

Result: `PASS`

The remediation changes only the private platform-side module-loading mechanism needed to execute the already-declared product-owned bridge. Tender Operator still consumes through the P6.02/CAP-001 seam and receives no access to P7.03 internals.

### Authority / governance

Result: `PASS`

No authorization, Organizational Authority, Data Governance or Consequential Approval semantics change. EIS remains the External Reference authoritative source.

### Security / effect boundary

Result: `PASS`

The failure was already fail-closed. The remediation does not add network, EIS/SOAP, canonical mutation or external-effect behavior. Existing guarded AST validation remains the supported pre-import operator boundary.

### Regression adequacy

Result: `PASS`

The new test exercises the precise unmocked failure mode: real dynamic execution of a slots dataclass bridge and successful module lookup through `sys.modules`.

### ADR / stable-boundary gate

Result: `PASS`

No ADR is required. The loader remains private, owner-local, reversible implementation below the existing Product Contract boundary and creates no public/stable module-loading API.

## 7. Remaining closure requirement

Repository remediation and CI are necessary but insufficient to close P7.07.

After the fix is reviewed, CI-passed and merged, the selected Mac must:

1. advance to the merged exact release through the existing P7.06 governed update path;
2. verify P7.03/P7.04 and the already-admitted exact P7.07 item/read grant remain intact;
3. rerun the guarded setup idempotently;
4. rerun `p7_07_guarded_selected_mac_proof.py`;
5. prove first real product consumption, supervised P7.02 restart, runtime instance replacement/generation continuity, byte-stable P7.03 state and the same exact CAP-001 reliance after restart;
6. retain bounded owner-local evidence and synchronize canonical roadmap/closure state only after that proof passes.

Until then `P7.07` remains `Current`; `P7.08` remains downstream.
