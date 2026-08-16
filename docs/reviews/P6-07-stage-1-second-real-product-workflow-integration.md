# P6.07 — Second real product/workflow platform integration — Stage 1 review

Status: `Complete / PASS (Stage 1)`  
P6.07 overall status: `In Progress`  
Date: `2026-08-16`  
Owner: ООО «Арвектум»

## 1. Governance basis

- Constitution: `1.2.0`, `Ratified`;
- task classification: `product_contract`, with secondary `product_specific` implementation evidence and `platform` validation;
- Accepted RFC checked: RFC-0001, RFC-0002, RFC-0003, RFC-0004, RFC-0005, RFC-0006;
- Accepted ADR relevant to this slice: none;
- canonical Product Contract: [`P6-06-SECOND-REAL-PRODUCT-CONTRACT.md`](../contracts/P6-06-SECOND-REAL-PRODUCT-CONTRACT.md), `Provisional 0.1.0`;
- shared dependency: CAP-004 Audit/Reconstruction Support, `Incubating / Provisional`, provider contract `1.0.0`.

No Constitution, Accepted RFC, Accepted ADR, capability lifecycle or Stable Product Contract change is made by this review.

## 2. Scope actually executed

P6.07 Stage 1 exercises the **Arvectum Discount Parser controlled Telegram publication workflow** as the second materially distinct product/workflow integration.

The proof is deliberately synthetic/offline:

1. the exact P6.06 Product Contract identity and version are projected into executable reference evidence;
2. only CAP-004 is declared and consumed;
3. product-owned references represent parse run, source observation, Offer, publication candidate, rule configuration, template version, pre-effect reservation/intent, Telegram target and publication outcome;
4. a product-owned fake Telegram adapter represents the external boundary without network access or credentials;
5. the resulting execution/effect evidence is reconstructed through the shared `IntegrationAdapters` CAP-004 seam;
6. exact Product Contract, Organization, Actor, correlation, causation and provenance continuity are retained.

No live Telegram publication, customer data mutation, product database migration, scheduler/autopost activation or reusable secret is part of Stage 1.

## 3. Executable evidence

Reference implementation:

- `reference/python/p6_07_discount_parser_ref/contract.py` — executable projection of P6.06 `Provisional 0.1.0` with CAP-004 only;
- `reference/python/p6_07_discount_parser_ref/journey.py` — product-facing reconstruction journey using only the shared `arvectum_os_ref.integration_adapters` boundary;
- `reference/python/p6_07_discount_parser_ref/scenario.py` — bounded offline controlled-publication scenario and product-owned fake Telegram adapter;
- `reference/python/tests/test_p6_07_second_real_product_workflow_integration.py` — positive and fail-closed architecture fitness evidence.

The Stage 1 tests prove at minimum:

- exact P6.06 Product Contract identity/version continuity;
- CAP-004-only dependency with CAP-001/CAP-002/CAP-003 absent;
- successful bounded offline publication evidence reconstruction;
- fail-closed behavior when required pre-effect evidence is unavailable;
- duplicate protection before any external send;
- explicit `uncertain/reconciliation-required` outcome with no blind retry;
- fail-closed behavior when the Product Contract version pin is missing;
- fail-closed behavior for wrong-Organization evidence;
- current CAP-004 provider evidence remains required after composition;
- no private platform module, live network library or secret-bearing configuration is introduced by the product-facing journey.

## 4. CI evidence

Pull request: `#16 — feat(p6.07): second real product workflow integration`.

GitHub Actions evidence at head `62adfbc81c512e07fcba5676d423f8a5b2f3d484`:

- `Reference Python CI #22`: `success`;
- job `Full reference test suite`: `success`;
- command: `python -m unittest discover -s tests -v`;
- result: `Ran 894 tests in 7.027s` / `OK`;
- all 10 `P607SecondRealProductWorkflowIntegrationTests` passed;
- `Mirror to GitVerse` for the same branch head also completed successfully.

## 5. Architecture result

### 5.1 Reuse result

**PASS.** The second materially distinct real-product workflow can reuse the existing shared integration boundary and CAP-004 semantic owner without a product-specific platform special case.

The product-facing journey imports only the shared `integration_adapters` surface. Discount Parser domain semantics remain outside `arvectum_os_ref`.

### 5.2 Platform-gap result

**No blocking platform gap was found in Stage 1.**

Therefore Stage 1 does not justify:

- a new RFC;
- a new ADR;
- a new Platform Capability;
- promotion of CAP-004 from `Incubating`;
- widening CAP-004's Provisional contract;
- moving Offer/source/dedup/classification/scheduler/rule-memory/Telegram semantics into the platform;
- creating a Stable/public API, SDK, wire protocol or product schema.

### 5.3 Failure semantics result

The second workflow adds materially different pressure — consequential external mutation, duplicate protection and an uncertain external outcome — while preserving the same platform principles:

- exact governed references instead of inferred current state;
- explicit Organization and Actor attribution;
- pre-effect evidence before consequential execution;
- no blind retry after an uncertain external outcome;
- reconstruction as derived read-oriented evidence, not replay or authority;
- product-owned external-system semantics remain product-owned.

## 6. What remains provisional

All of the following remain provisional after Stage 1:

- P6.06 Product Contract `0.1.0`;
- CAP-004 lifecycle and provider contract;
- the Python/dataclass/module spelling of this reference implementation;
- the fake Telegram adapter;
- the exact future implementation mechanism used by Discount Parser to emit platform evidence.

This review does not establish production readiness, SLA/support commitments, public compatibility, full-platform conformance or capability activation.

## 7. Stage 2 gate

P6.07 is **not complete overall** because Stage 1 intentionally performs no real Telegram side effect.

The next bounded action remains the P6.06 Stage 2 gate: one explicitly authorized, human-operated real publication for one Organization and one authorized Telegram channel, with:

1. attributable human Actor context;
2. exact P6.06 Product Contract `0.1.0` pin;
3. selected publication candidate and target;
4. durable pre-effect intent/reservation evidence;
5. one controlled external send;
6. confirmed external message/effect reference or explicit uncertain outcome;
7. CAP-004 reconstruction of the exact execution/effect evidence;
8. no scheduler/autopost enablement as part of the proof.

Stage 2 must not be inferred from this offline evidence and must not be fabricated in documentation.

## 8. Decision

`P6.07 Stage 1 = Complete / PASS`.

`P6.07 overall = In Progress` until the explicitly authorized real Stage 2 publication is executed and reconstructed.

Phase 6 remains `Active / In Progress`.
