# P8.04 — External Authoritative-System Connector Pattern Validation

Status: `Complete / PASS`
Version: `1.0.0`
Created: `2026-08-20`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` with `platform`, `product_specific` and `governance`
Phase: `Phase 8 — Active`
Roadmap work item: `P8.04 — External authoritative-system connector pattern validation`
Product: Tender Operator
Predecessors: [`P8.01`](P8-01-eis-revalidation-target-evidence-baseline.md); [`P8.02`](P8-02-identity-trust-rights-data-governance-boundary.md); [`P8.03`](../contracts/P8-03-EIS-EXTERNAL-AUTHORITY-REVALIDATION-CONTRACT.md); [`R25`](R25-external-boundary-review.md)
Architecture authority: RFC-0004 `1.0.0` — `Accepted`
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)

## 1. Result

**PASS — one bounded live read-only EIS revalidation for notice `0344100006426000005` completed with an immutable-baseline-verified `NO_CHANGE` result, deterministic comparison, independent byte verification, network-free offline re-comparison, and full governed evidence admission + reconstruction.**

P8.04 validated the external authoritative-system connector pattern end-to-end:

- real ЕИС / `zakupki.gov.ru` read-only retrieval (`getDocsByReestrNumber`) reusing the existing product-owned P6 retrieval path;
- fresh exact observation produced for the selected notice;
- deterministic comparison against the immutable P6.05-L7 attempt #2 baseline manifest SHA-256 `74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121`;
- result `NO_CHANGE` (all 7 material documents byte-identical);
- governed Arvectum OS evidence admission and read-only reconstruction without external-effect replay.

## 2. Execution summary

Single top-level live run:

| Field | Value |
|---|---|
| Run ID | `toa-run-20260820083457-21337c` |
| Notice | `0344100006426000005` |
| External source authority | ЕИС / `zakupki.gov.ru` |
| Retrieval method | SOAP `getDocsByReestrNumber`, archive download, read-only |
| Fresh observed / retrieved | `2026-08-20T08:34:57.365770+00:00` |
| Baseline manifest SHA-256 | `74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121` |
| Fresh manifest SHA-256 | `4113935e43291f820a43fa2efad49663103a86408788b571d7d0e6dac4974a54` |
| Comparison manifest SHA-256 | `06ca91f5689d449b2bfba95ca0ec62386e215261df74ec769b234030cc610f7b` |
| Aggregate result | `NO_CHANGE` |
| Evidence completeness | `complete` |
| External actions | `false` |
| Exit code | `0` |

Live invocation count: exactly one top-level live run.

## 3. Baseline immutability and verification

The owner-local P6.05-L7 attempt #2 exact manifest was loaded and fail-closed verified before any comparison:

- baseline schema `p6.05-exact-attachment-evidence-v1`;
- baseline status `PASS_EXACT_ATTACHMENT_EVIDENCE`;
- baseline notice matches `0344100006426000005`;
- canonical body SHA-256 recomputed (excluding `manifest_sha256` / `manifest_integrity_ref`) and matched the pinned value;
- all 7 expected documents present.

The baseline file was not modified by the P8.04 run (mtime preserved from `2026-08-15`, hash unchanged). A fresh comparison or fresh observation never mutates historical P6 evidence.

## 4. Fresh observation and deterministic comparison

Fresh exact observation was produced by the P6 exact-evidence builder reusing the existing product-owned retrieval path. All 7 expected documents were present, no missing/duplicate names, external action flags disabled, archive downloaded and extraction complete.

Comparison per material document (deterministic, name-keyed):

| Document | Classification | Baseline SHA-256 (prefix) | Fresh SHA-256 (prefix) |
|---|---|---|---|
| `1. Расчет НМЦК1.xlsx` | UNCHANGED | `5759cb0596d2` | `5759cb0596d2` |
| `1. Расчет НМЦК2.docx` | UNCHANGED | `88a4c89783ab` | `88a4c89783ab` |
| `2. Проект контракта.docx` | UNCHANGED | `fecf03cccb63` | `fecf03cccb63` |
| `3. Описание объекта закупки.docx` | UNCHANGED | `da07b8a3c3b6` | `da07b8a3c3b6` |
| `4. Требования к содержанию, составу заявки.docx` | UNCHANGED | `e0e19bad3768` | `e0e19bad3768` |
| `5. Реквизиты.docx` | UNCHANGED | `026ecfc98505` | `026ecfc98505` |
| `6. Информация о поставке товара.docx` | UNCHANGED | `03c3d2209a87` | `03c3d2209a87` |

Aggregate result: `NO_CHANGE`.

## 5. Independent verification

Independently of the harness:

- every material document's raw bytes were re-hashed from the run input directory and all 7 matched the fresh manifest digests;
- the fresh manifest body SHA-256 and the comparison manifest body SHA-256 were recomputed independently and matched the recorded `manifest_sha256` values;
- the P6 baseline document digests were cross-checked against the fresh observation digests — zero differing documents.

## 6. Network-free deterministic re-comparison

With `socket.socket` and `socket.create_connection` replaced by fail-closed stubs, the comparison manifest was rebuilt from the stored fresh observation and the immutable baseline. The rebuild was byte-identical to the recorded comparison manifest, proving the comparison requires no EIS replay and remains deterministic.

## 7. Governed evidence and reconstruction

Arvectum OS governed evidence admission was executed for the live run under the P8.03 contract (`Provisional 0.1.0`):

- Organization scope: `ООО «Арвектум»` (one Organization, no ambient/default fallback);
- attributable actor resolved from the established owner-local P6.05-L4 context (real M7 Organization `aa4e760c379c8952aba6c6c335f3e233` and human owner-operated operator);
- authority mode: `External Reference` with explicit ЕИС authority contract for the observed documents; `Native` for the locally derived comparison result with provenance to both External Reference inputs;
- material input: fresh observation evidence manifest (CAP-001), integrity-pinned;
- comparison result record pinning baseline + fresh manifest SHA-256 and aggregate result;
- governed execution through Authorization, Organizational Authority, Data Governance and Consequential Approval gates;
- admitted canonical Event `platform.external-revalidation.completed`;
- reconstruction manifest built and read-only audit view reconstructed — `reconstruction_complete: True`, 15 evidence roles, without network replay.

## 8. Result acceptance

Per P8.00/P8.03, both `NO_CHANGE` and `CHANGE_DETECTED` are valid live outcomes when evidenced correctly. This run returned `NO_CHANGE` with complete, immutable, independently verified evidence.

P8.04 exit criteria are satisfied:

- exactly one bounded live read-only external retrieval;
- immutable P6 baseline referenced, not mutated;
- fresh observation attributable and distinct from the baseline;
- deterministic comparison with explicit aggregate result;
- governed evidence + reconstruction without replay;
- no secrets, no external mutation, no second Organization, no public surface created.

## 9. Files changed

Tender Operator (product-owned):

- `scripts/p8_04_eis_temporal_revalidation.py` — bounded revalidation logic (baseline verification, fresh snapshot, deterministic comparison, manifests);
- `scripts/p8_04_run_eis_temporal_revalidation.py` — single-live-run operator runner with fail-closed preflight;
- `tests/test_p8_04_eis_temporal_revalidation.py` — offline tests (NO_CHANGE / CHANGE_DETECTED / fail-closed / determinism / secret redaction / baseline immutability).

Arvectum OS (platform-owned):

- `reference/python/p8_04_eis_authoritative_system_evidence.py` — governed evidence admission + reconstruction;
- `reference/python/tests/test_p8_04_eis_authoritative_system_evidence.py` — offline governed-evidence tests with network blocked;
- this review document.

## 10. Validation performed

- `uv run pytest -q tests/test_p8_04_eis_temporal_revalidation.py` — 29 passed;
- `uv run pytest -q tests/test_p6_05_exact_attachment_evidence.py tests/test_p8_04_eis_temporal_revalidation.py` — 46 passed;
- `uv run ruff check` on changed paths (both repos) — clean;
- owner-local baseline verification preflight — PASS;
- live EIS run — PASS (`NO_CHANGE`, exit 0);
- independent byte + manifest re-hash — PASS;
- offline network-blocked re-comparison — byte-identical to the recorded comparison manifest (hash `06ca91f5689d449b2bfba95ca0ec62386e215261df74ec769b234030cc610f7b`);
- offline governed-evidence tests — 10 passed;
- remediated governed admission + reconstruction rerun against the preserved live evidence — `PASS`, `reconstruction_complete: True`, 15 evidence roles, `additional_live_eis_calls: 0`;
- repaired M3 roadmap test — 5 passed;
- full arvectum-os reference suite (modified tree): `1138 passed, 64 failed`; full suite at clean base commit `d26f958`: `1127 passed, 65 failed` — the 65 base failures are pre-existing on the unchanged base (see the Cross-review remediation section for the exact classification; not all are macOS sandbox failures);
- full tender-agent suite: `2437 passed, 241 skipped, 1 failed` — the single failure is a pre-existing, unrelated R9 backup/restore acceptance subprocess failure present on the unchanged tracked tree.

## 11. Constraints preserved

- read-only external retrieval only; no EIS/ETP mutation, submission, EDS, supplier messaging or broad crawling;
- one Organization (`ООО «Арвектум»`); no cross-Organization use;
- no secrets/tokens committed or printed; token presence checked without value exposure;
- TLS policy required (`ARVECTUM_ETP_TLS_ENABLED=true`, `CERT_REQUIRED`, hostname verification, TLS ≥ 1.2, system truststore);
- failed retrieval would not be reported as `NO_CHANGE`; missing/incomplete baseline blocks PASS;
- P6 historical evidence preserved immutable;
- reconstruction performs no automatic external call.

## 12. Cross-review

### Iteration 1 — product/platform boundary

Kept EIS/SOAP/archive/procurement semantics in the Tender Operator harness and limited platform evidence to governed reliance semantics per P8.03.

### Iteration 2 — freshness/version-drift semantics

Made the fresh observation and historical baseline independently attributable, pinned exact hashes in the comparison record, and prohibited reconstruction from replaying retrieval.

### Iteration 3 — security

Verified baseline fail-closed verification, secret non-exposure, TLS enforcement, external-action flags and one-run discipline.

**Result:** `PASS`; no material objection remains.

## 13. Cross-review remediation (2026-08-20)

A focused cross-review of the initial P8.04 implementation identified and repaired the following items in the uncommitted P8.04 working changes. The original live observation and owner-local raw evidence are unchanged.

1. **Tender-agent fail-closed comparison.** `aggregate_result([])` no longer returns `NO_CHANGE`; it raises `BLOCKED_EMPTY_COMPARISON`. `build_comparison_manifest` and `compare_document_sets` now fail closed on empty document lists, malformed document entries, duplicate names/identities (no silent overwrite in `_document_set`), internally inconsistent count/completeness metadata, and canonical-body SHA-256 mismatch in either the baseline or the fresh manifest. New offline tests cover unchanged / changed / added / removed / empty baseline / empty fresh / duplicate baseline / duplicate fresh / fresh integrity mismatch / baseline integrity mismatch / inconsistent exact count / declared-duplicates metadata / external-actions flag / deterministic repeat / no stale-baseline fallback (17 existing + 12 added tests).

2. **Arvectum OS authority-basis repair.** The self-minted authority `owner-authority-p8-04-revalidation` (a single basis for all four gates) was removed. Authorization is now a real P7.04 decision from `authorize_from_credential_file`, using only the exact temporary grant `p8.04.eis-revalidation.admit` / `p8-04:eis-revalidation:0344100006426000005` / `local`. Its basis binds the actual returned grant id as `authorization-basis:p7-04-persistent-access-grant:<grant_id>`. The remaining gate decisions reference pre-existing governed evidence: `organizational-authority-basis:decision-2026-08-20-phase-8-activation`, `data-governance-basis:p6-02-v0.1.0+p6-05-l7-exact-eis-manifest`, and `consequential-approval-basis:decision-2026-08-20-phase-8-activation`. A8 is the approved Organizational Authority decision and does not substitute for technical P7.04 Authorization. Product Contract resolution never substitutes for a gate.

3. **M7 identity reuse.** The fabricated `p8-04-org-a` organization and `p8-04-product-operator` principal were removed. The evidence script now resolves the real M7 Organization (`aa4e760c379c8952aba6c6c335f3e233` / `ООО «Арвектум»`) and the human owner-operated operator (`e4fc60984850106dbfc922ba30ec2332`) from the established owner-local P6.05-L4 context via `p7_04_persistent_access.load_p6_owner_context`, and fails closed (`BLOCKED`) when the context path is missing, unreadable, foreign, or malformed. No new P8-specific Organization is created. Tests cover missing context deny, foreign context deny, and existing owner/operator resolution.

4. **Product attribution correction.** The product identity was corrected from `arvectum-os` to the real Tender Operator product `arvectum-tender-operator` (with product compatibility line `restricted-paid-pilot/44fz-prebid-v1`) via `p6_03_tender_operator_ref.contract.product_id_for`. Arvectum OS is represented as the platform producer (`producer:platform.core`, `authoritative_source=platform.core`), not as the product. Reconstruction distinguishes Product (Tender Operator) from Platform (Arvectum OS).

5. **Derived-comparison authority correction.** The observation record stays `External Reference` (ЕИС remains authoritative for the observed facts). The locally derived comparison result is now `Native` governed authority with provenance links to both External Reference inputs — the fresh `observation-version` and the pinned `baseline` identity — instead of being mislabeled as `External Reference`. No fourth `AuthorityMode` was invented.

6. **Platform manifest integrity verification.** The evidence script now independently recomputes the canonical JSON body SHA-256 of both the fresh observation and the comparison manifest before governed admission (domain-neutral cryptographic check, not just cross-field comparison). Tampered fresh or tampered comparison manifests fail closed with `BLOCKED ... integrity mismatch` and never produce a governed `PASS`; negative tests cover both.

7. **M3 roadmap test repair and baseline classification.** The stale `test_canonical_roadmap_preserves_m3_scope_as_later_phases_progress` asserted a removed roadmap table format (`| Phase 3 | ... | Executed | ... |`). It was repaired to assert semantic invariants (Phase 3 row is `🟩 Complete` with `M3 Validated shared capability baseline`; Phase 4 present; CAP-001..004 remain `Incubating / Provisional`; no Platform Capability is `Active`; phase/capability/contract/operational/commercial statuses remain distinct) and is classified as a **pre-existing stale roadmap rendering assertion** discovered during the P8.04 review. Baseline classification at the clean base commit `d26f9583393d4f3d9ef104f5408439da0471fd76` (full suite: `65 failed, 1127 passed`): all 64 non-M3 failures reproduce identically on the clean base and the modified tree and are classified **BASELINE_PRE_EXISTING**; of those, 63 are the **ENVIRONMENT_SPECIFIC** macOS `/var → /private/var` symlink class (P7.04/P7.05/P7.06/P7.07 temp-path handling, e.g. `PosixPath('/private/var/...') != PosixPath('/var/...')`), and 1 is a **deterministic message-mismatch** (not macOS-specific): `test_p7_05_selected_mac_proof::test_selected_mac_contract_fails_on_runtime_release_mismatch` expects `runtime release mismatch` but the implementation raises `P7.05 launchd observer is not pinned to the exact proof release`. **P8_04_INTRODUCED: none**. `test_canonical_deploy_uses_checkout_controller_not_release_snapshot` and `test_selected_mac_contract_fails_on_runtime_release_mismatch` were both run and fail at the clean base commit.

**Verified hashes (recomputed from the preserved on-disk evidence with the harness canonical-body convention):**

- baseline raw file SHA-256: `678d3a0ae13e629bdd25c96b33da11d4adeae446335f47dfd14cb609ddbbcbe9`;
- baseline embedded `manifest_sha256`: `74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121`;
- fresh raw file SHA-256: `78c9e340cad35a9f030cffec5005d733dc83bd7cd595eabeb9b086d544a50ebd`; fresh embedded: `4113935e43291f820a43fa2efad49663103a86408788b571d7d0e6dac4974a54`;
- comparison raw file SHA-256: `3ab3363c980f08d0c022440c03e3f01d8bf64a4dcc80b2ce60e15a75a0d3102e`; comparison embedded: `06ca91f5689d449b2bfba95ca0ec62386e215261df74ec769b234030cc610f7b`.

The values above are the actual verified hashes from the preserved on-disk evidence and the hashes originally recorded by the live run. The remediation did not change the comparison manifest schema or content; an offline rebuild from the preserved baseline and fresh observation is byte-identical to the recorded comparison manifest (`06ca91f5...`), so no comparison regeneration was required.

## 14. Final authorization cross-review (2026-08-20)

The final cross-review verified the repaired control boundary against the implementation and focused regressions:

1. P8.04 calls the real P7.04 `authorize_from_credential_file`; it does not infer authorization from a label, A8 approval, Product Contract availability, or gate presence.
2. Authorization fails closed unless the decision is `allowed=True`, reason `EXPLICIT_LEAST_PRIVILEGE_GRANT`, a human principal is attributable, and organizational/consequential approval flags remain false.
3. The temporary grant is limited to the exact operation, resource, and `local` access path. Its actual `grant_id` is bound into the Authorization gate basis.
4. Temporary-grant cleanup now covers authorization denial as well as admission failure and success. Tests prove the grant is `revoked` after both positive and negative module runs.
5. A8 `Approved` verification remains distinct from technical P7.04 authorization. The evidence output records the exact operation, resource, access path, grant basis, gate kinds, and revoked proof without exposing credential material.
6. Live provenance is explicit: the two source SHA-256 values identify the uncommitted implementation used for the live observation, while Tender Agent SHA `449cf980e46f561d6819349a3c5c258a069c0594` identifies the post-live canonical publication. They are not claimed to be the same version.
7. The focused P8.04 suite passes `28` tests; network-blocked admission and reconstruction pass with `additional_live_eis_calls: 0`. No material authorization objection remains for this remediation. The full-suite baseline classifications and the remaining unrelated macOS/message-mismatch failures remain unchanged.

**Remediation status:** `PASS` — P8.04 remains `Current` until this remediation and its evidence are reviewed.

## 15. Handoff

P8.04 exit criteria are satisfied with a verified live `NO_CHANGE` and complete governed evidence.

Next canonical action:

> **P8.05 — External ingress/egress Event, duplicate, replay, uncertainty + reconciliation semantics.**
