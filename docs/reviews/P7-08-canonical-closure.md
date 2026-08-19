# P7.08 — Canonical Closure

- **Task:** `P7.08 — Persistent Discount Parser cross-host operational contour`
- **Status:** `Complete / PASS`
- **Date:** `2026-08-19`
- **Operating scope:** `Persistent Internal / owner-operated`
- **Task classification:** `product_contract` (secondary: `product_specific`, bounded platform integration evidence)
- **Implementation PR:** `#78`
- **Canonical merge:** `fefbea71a1f3941275faa6313e162f0040fecb8d`
- **Final implementation head:** `8934b44c8156faf937fc3e1cfaf793d05508414e`
- **Reference Python CI:** `#159` / run `32245986650` — `success`
- **Canonical Product Contract:** `docs/contracts/P6-06-SECOND-REAL-PRODUCT-CONTRACT.md` `0.1.0` / `Provisional`
- **Shared platform dependency:** `CAP-004` only
- **Implementation:** `reference/python/p7_08_discount_parser_cross_host.py`
- **Regression coverage:** `reference/python/tests/test_p7_08_discount_parser_cross_host.py`

## Closure result

P7.08 is closed for the declared `Persistent Internal / owner-operated` scope.

The merged contour makes the Discount Parser Windows ↔ Mac mini evidence/reconstruction path repeatable as three explicit steps:

1. **Mac mini `issue`** — creates the identity-bearing P6.07-compatible Stage 2A ticket in Mac-private storage and emits a minimized dispatch containing only execution/ticket digest, exact Product Contract pin, release reference and safety boundary;
2. **Windows `handoff`** — verifies owner-local pre-effect/outcome evidence by SHA-256, validates strict product-owned publication evidence, keeps raw evidence and product state local, and emits a minimized handoff containing only stable references and digests;
3. **Mac mini `reconstruct`** — verifies exact round-trip continuity, restores Organization/Actor context from the Mac-private ticket, asserts exact P6.06 `0.1.0` and CAP-004-only reliance, then performs read-only CAP-004 reconstruction without replaying Telegram or any other product/external effect.

## Exact boundary preserved

No P6.06 Product Contract revision was required or made.

The closure preserves:

- Product Contract lifecycle: `Provisional 0.1.0`;
- shared dependency set: exactly `{CAP-004}`;
- Discount Parser ownership of Offer/publication/product DB/Telegram integration;
- Arvectum OS reconstruction as `ReadOnly` support rather than product truth or external-effect authority;
- no CAP-001/CAP-002/CAP-003 reliance;
- no new platform transport service, shared database, broker, stable public API or Platform Capability;
- no lifecycle promotion, Production claim, SLA/support commitment or broader conformance claim.

## Cross-host minimization and security

The final contour proves the required asymmetric boundary:

- Organization and attributable human Actor identity remain in the Mac-private Stage 2A ticket and are not transferred to Windows;
- reusable secrets are rejected from transferable dispatch/handoff evidence;
- raw Windows pre-effect/outcome evidence remains Windows-local;
- Windows product database state is not transferred;
- Mac receives hashes plus minimized exact references, not raw product evidence;
- transfer evidence is immutable JSON + SHA-256 sidecar pairs rather than mutable shared state;
- the transport mechanism remains operator-selected and outside the Product Contract/platform capability surface.

## Replay / uncertainty safety

The contour fails closed when:

- external outcome is not explicitly confirmed;
- `reconciliation_required=true`;
- dispatch/handoff/evidence digest verification fails;
- target/template provenance references do not exactly match their declared values;
- a completed execution is presented with a different handoff;
- reconstruction state is partial or internally inconsistent.

The same already-completed verified handoff is treated idempotently as `ALREADY_RECONSTRUCTED`. Historical reconstruction never calls Telegram, Discount Parser publication code or any other external mutation. A new real effect still requires a new execution and applicable authorization.

## Functional cross-review closure

Four implementation review/revise iterations closed all material objections:

1. **Product/platform boundary:** replaced historical one-off constants with execution-specific evidence while retaining the exact Product Contract and CAP-004-only boundary.
2. **Identity/security:** kept identity-bearing Stage 2A evidence Mac-private and transferred only digest/execution continuity.
3. **Replay/partial-state safety:** required a complete verified report+receipt set for idempotent completion; partial/conflicting state fails closed.
4. **Provenance continuity:** required exact equality of `telegram-target ↔ target_ref` and `template-version ↔ template_version`.

The first CI attempt exposed one test-only type assertion (`Identity` compared to string). The test was corrected to assert `CAP_004_AUDIT_RECONSTRUCTION.value == "CAP-004"`; no implementation or architecture change was required. Final Reference Python CI `#159` completed with `success` on implementation head `8934b44c8156faf937fc3e1cfaf793d05508414e` before PR #78 was merged.

**Remaining material objections:** none.

## Read-after-write verification

After PR #78 merge, canonical `main` at merge `fefbea71a1f3941275faa6313e162f0040fecb8d` was read back and confirmed to contain `reference/python/p7_08_discount_parser_cross_host.py` with the intended three-step Mac → Windows → Mac contour, exact P6.06 boundary and CAP-004-only description.

This closure is repository/operational-contour closure for the declared owner-operated scope. It does not claim that a separate live customer or externally hosted Production deployment has occurred.
