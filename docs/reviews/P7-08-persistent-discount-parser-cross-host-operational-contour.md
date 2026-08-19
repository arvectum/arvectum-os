# P7.08 — Persistent Discount Parser cross-host operational contour

- **Task:** P7.08
- **Status:** Implementation review — CI pending
- **Date:** 2026-08-19
- **Operating scope:** `Persistent Internal / owner-operated`
- **Task classification:** `product_contract` (secondary: `product_specific`, bounded platform integration evidence)
- **Canonical Product Contract:** `docs/contracts/P6-06-SECOND-REAL-PRODUCT-CONTRACT.md` `0.1.0` / `Provisional`
- **Shared platform dependency:** `CAP-004` only
- **Implementation:** `reference/python/p7_08_discount_parser_cross_host.py`
- **Regression coverage:** `reference/python/tests/test_p7_08_discount_parser_cross_host.py`

## 1. Objective

Make the Discount Parser Windows ↔ Mac mini evidence/reconstruction path operationally repeatable without converting the P6.07 one-off proof into a hidden transport service, shared mutable database, stable public API or new platform capability.

The contour MUST preserve:

- the exact applicable P6.06 Product Contract boundary;
- CAP-004-only shared platform reliance;
- exact Organization and attributable human Actor continuity on the Arvectum OS side;
- minimized cross-host evidence transfer;
- no reusable-secret transfer;
- no raw Organization/Actor identity transfer;
- no raw Windows product evidence transfer;
- no replay of the Telegram external effect;
- explicit fail-closed handling of uncertain outcomes and conflicting replays;
- product ownership of Discount Parser domain state and Telegram integration.

## 2. Governance decision

No Product Contract revision is justified by P7.08.

P6.06 `0.1.0` already permits the required read-only CAP-004 reconstruction path and already requires the exact product evidence references used here. P7.08 therefore operationalizes the existing boundary instead of broadening it.

This task does **not**:

- add CAP-001, CAP-002 or CAP-003;
- promote CAP-004 lifecycle state;
- move Discount Parser business logic into the platform;
- make the Windows host a platform authority;
- make Arvectum OS authoritative for Discount Parser Offer/publication truth;
- create a stable cross-host transport API;
- create canonical Events merely because local reconstruction material exists;
- grant authorization for Telegram publication;
- claim Production, SLA/support or conformance promotion.

## 3. Operational shape

The repeatable path is deliberately three-step and asymmetric.

### Step A — Mac mini: issue execution intent

The Mac mini runs `issue` before the real product-side effect.

It writes the existing Stage 2A ticket under an execution-specific Mac-private directory:

```text
<RUNTIME_ROOT>/product-contours/discount-parser/runs/<execution_id>/mac-private/
  p6-07-stage2-execution-ticket.json
  p6-07-stage2-execution-ticket.sha256
```

The ticket contains exact Organization/Actor continuity and remains Mac-private.

The same command emits a minimized outbound dispatch:

```text
<RUNTIME_ROOT>/product-contours/discount-parser/runs/<execution_id>/outbound/
  p7-08-discount-parser-dispatch.json
  p7-08-discount-parser-dispatch.sha256
```

Only this dispatch pair is transferred to Windows. It contains the execution id, exact Stage 2A ticket digest, exact P6.06 Product Contract pin, CAP-004-only dependency declaration and safety boundary. It contains no raw Organization/Actor identity and no reusable secret.

Example invocation:

```bash
python reference/python/p7_08_discount_parser_cross_host.py issue \
  --runtime-root "$ARVECTUM_RUNTIME_ROOT" \
  --organization-id <owner-organization-id> \
  --actor-id <attributable-human-actor-id> \
  --canonical-repo-sha <40-char-arvectum-os-sha>
```

### Step B — Windows: bind local product evidence and create minimized handoff

The Windows host remains the owner of the raw Discount Parser pre-effect/outcome evidence and product database.

The operator provides:

1. the exact dispatch JSON + SHA-256 sidecar received from Mac;
2. a strict Windows-local descriptor containing only the P6.06-required product references and bounded-publication outcome fields;
3. raw pre-effect evidence + its locally retained SHA-256 sidecar;
4. raw confirmed outcome evidence + its locally retained SHA-256 sidecar.

The harness verifies the raw evidence digests but never parses or embeds the raw files in transferable evidence.

Example invocation:

```powershell
python reference/python/p7_08_discount_parser_cross_host.py handoff `
  --dispatch <dispatch.json> `
  --dispatch-digest <dispatch.sha256> `
  --descriptor <windows-local-descriptor.json> `
  --pre-effect <pre-effect.json> `
  --pre-effect-digest <pre-effect.sha256> `
  --outcome <outcome.json> `
  --outcome-digest <outcome.sha256> `
  --output-dir <handoff-output-dir>
```

The only Windows → Mac transfer is:

```text
p7-08-discount-parser-handoff.json
p7-08-discount-parser-handoff.sha256
```

The handoff contains hashes and minimized stable references, not raw evidence, credentials, product DB state, Organization identity or Actor identity.

### Step C — Mac mini: CAP-004 reconstruction

The Mac mini runs `reconstruct` with the returned handoff pair.

The harness:

1. verifies the handoff SHA-256;
2. resolves the execution-specific local dispatch and verifies exact round-trip continuity;
3. resolves and verifies the Mac-private Stage 2A ticket;
4. restores exact Organization/Actor context in memory only;
5. composes the exact executable P6.06 Product Contract projection;
6. asserts that the dependency set is exactly `{CAP-004}`;
7. reconstructs the confirmed publication through CAP-004 as `ReadOnly`;
8. writes an identity-minimized non-canonical operational report and immutable receipt;
9. treats the same verified handoff as idempotently already reconstructed;
10. rejects a different handoff for an execution that already has a completed receipt.

Example invocation:

```bash
python reference/python/p7_08_discount_parser_cross_host.py reconstruct \
  --runtime-root "$ARVECTUM_RUNTIME_ROOT" \
  --handoff <returned-handoff.json> \
  --handoff-digest <returned-handoff.sha256> \
  --canonical-repo-sha <40-char-arvectum-os-sha>
```

The Mac-local output is:

```text
<RUNTIME_ROOT>/product-contours/discount-parser/runs/<execution_id>/reconstruction/
  p7-08-discount-parser-reconstruction.json
  p7-08-discount-parser-reconstruction.sha256
  p7-08-discount-parser-reconstruction-receipt.json
  p7-08-discount-parser-reconstruction-receipt.sha256
```

These files are non-canonical operational evidence. They do not by themselves create a Native canonical Event or mutate canonical organizational state.

## 4. Windows-local descriptor boundary

The descriptor is a task-local/product-local evidence shape, not a Stable platform API. Unknown top-level fields fail closed.

Required semantic groups:

- product repository + exact product Git SHA;
- ready text-only publication candidate;
- exact Telegram target reference;
- exact template version;
- explicit one-time human authorization evidence;
- scheduler/autopost containment and exactly one text send path;
- pending pre-effect publication reservation;
- confirmed published outcome with `reconciliation_required=false`;
- material refs required by P6.06:
  - source observation;
  - offer;
  - publication candidate;
  - rule/filter configuration;
  - template version;
  - publication reservation;
  - publication attempt;
  - Telegram target;
  - authorization evidence;
  - optional parse-run/source refs.

The `telegram-target` material reference must equal `target_ref`; the `template-version` material reference must equal `template_version`.

## 5. Cross-host minimization

### Mac → Windows

Transferred:

- execution id;
- Stage 2A ticket SHA-256;
- exact Product Contract version/blob pin;
- `CAP-004` dependency declaration;
- Arvectum OS ticket-issuer repository SHA;
- declarative cross-host safety boundary.

Not transferred:

- Organization identity;
- Actor/principal identity;
- Stage 2A ticket body;
- reusable secret;
- platform internal state.

### Windows → Mac

Transferred:

- exact execution/dispatch/ticket continuity digests;
- product repo SHA;
- minimized product evidence references;
- pre-effect/outcome SHA-256 digests;
- bounded authorization/containment facts;
- confirmed external outcome references.

Not transferred:

- raw pre-effect evidence;
- raw outcome evidence;
- Windows product database;
- Telegram credential/token;
- raw Organization/Actor identity;
- arbitrary Windows environment/configuration.

## 6. Replay and uncertainty rules

P7.08 is reconstruction-only after the product-side external effect.

- Reconstruction never calls Telegram.
- Reconstruction never invokes Discount Parser publication code.
- A reconstructed historical effect is never repeated.
- `external_confirmation != PASS` fails closed.
- `reconciliation_required = true` fails closed.
- A second read of the exact same completed handoff returns `ALREADY_RECONSTRUCTED` after verifying receipt/report integrity.
- A different handoff for the same completed execution fails closed as ambiguous replay.
- Partial local reconstruction state fails closed and requires operator reconciliation; it is not silently overwritten.
- New external effects always require a new execution id and new explicit real-action authorization through the applicable governed path.

## 7. Hidden-state check

No mutable cross-host shared state is introduced.

- Windows raw evidence remains Windows-local.
- Mac private identity-bearing ticket remains Mac-local.
- Transfer is explicit immutable file-pair movement chosen by the owner/operator.
- No shared network filesystem, database, broker, internal table access or undocumented API is required.
- The transport mechanism itself is intentionally outside the Product Contract and platform capability surface.

## 8. Functional cross-review

### Iteration 1 — product/platform boundary

**Finding:** Reusing the original P6.07 Stage 2C constants would make the contour permanently bound to one historical publication.

**Revision:** P7.08 introduces a dynamic execution-specific dispatch/handoff while keeping the exact P6.06 Product Contract and CAP-004-only dependency.

### Iteration 2 — identity/security

**Finding:** Copying the Stage 2A ticket to Windows would unnecessarily transfer Organization/Actor identity.

**Revision:** the identity-bearing ticket remains Mac-private; Windows receives only its digest and execution id. Transfer evidence rejects raw Organization/Actor fields and reusable-secret markers.

### Iteration 3 — replay/partial-state safety

**Finding:** A receipt alone is insufficient if its report is missing or corrupted; a retry could otherwise conceal partial local state.

**Revision:** completed replay is accepted only when report + report digest + receipt + receipt digest all exist, verify, and bind the same handoff. Partial state fails closed. Conflicting handoff replay fails closed.

### Iteration 4 — material-reference continuity

**Finding:** Merely requiring the presence of target/template material roles would permit mismatch between declared top-level target/template and the provenance references.

**Revision:** exact equality is now required for `telegram-target` ↔ `target_ref` and `template-version` ↔ `template_version`.

**Current material objections:** none identified in implementation review. CI remains required before closure.

## 9. Regression intent

The P7.08 regression suite covers:

- Mac-private identity retention and minimized dispatch;
- raw-evidence hash binding without raw transfer;
- exact P6.06 version/blob pin and CAP-004-only dependency;
- reusable-secret fail-closed behavior;
- uncertain external outcome fail-closed behavior;
- dispatch tamper detection;
- end-to-end CAP-004 reconstruction;
- identity-minimized reconstruction report;
- no external mutation / no Telegram replay;
- idempotent same-handoff reconstruction;
- conflicting completed-execution handoff rejection;
- source-level absence of live network / Telegram effect paths.

## 10. Closure gate

P7.08 may be marked `Complete / PASS` only after:

1. branch tests/CI pass;
2. read-after-write inspection confirms the intended code and review artifact;
3. no material functional cross-review objection remains;
4. the branch is merged to canonical `main`;
5. resulting canonical state is verified;
6. `docs/roadmap/ROADMAP.md` is synchronized and P7.09 becomes the next canonical action.
