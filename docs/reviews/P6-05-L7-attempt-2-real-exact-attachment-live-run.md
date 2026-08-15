# P6.05-L7 attempt #2 — real exact-attachment live run (PASS)

* Status: `Complete / PASS`
* Date: `2026-08-15`
* Owner: `ООО «Арвектум»`
* Task classification: `platform` with `product_contract` and `product_specific`
* Operational Environment: `Internal / local owner-operated runtime`
* Production-readiness claim: `None`
* Platform execution SHA: `5480f282cf8b3ec786b658f431e2fc0225afe257`
* Product execution SHA: `33721ab63ffe8bcd1178b119c488a54fcb1b1748`
* Attempt number: `2`
* Prior attempt: attempt #1 FAIL-CLOSED on EIS TLS trust (blocker review [`P6-05-L7-attempt-1-eis-tls-trust-blocker.md`](P6-05-L7-attempt-1-eis-tls-trust-blocker.md))

## 1. Attempt #2 execution facts

- Exactly one top-level execution of `scripts/p6_05_capture_real_attachment_evidence.py` on canonical product main; no second invocation, no manual SOAP/archive repetition, no `runner.main()` call.
- Notice `0344100006426000005`, law `44-ФЗ`, subsystem `PRIZ`, SOAP method `getDocsByReestrNumber`, `download_archive=True`, `analyze_after_download=False` (preserved from source).
- Owner-operated ETP trust remediation was active for this process: `authority: system` (truststore), `direct_connection=true`, proxy bypass enabled.
- `CERT_REQUIRED`, hostname verification, and TLS >= 1.2 preserved; no custom CA; no OS trust/keychain mutation; no certificate verification weakened.
- Read-only `getDocsIP` SOAP request executed and completed; archive URL returned; archive downloaded (internal download attempts: 1, `archive_download_status=downloaded`); safe local ZIP extraction completed; exact evidence manifest generated.
- Product analysis executed: NO (`analysis_status=not_started`, `requested_analyze_after_download=false`).
- `external_actions=false`, `no_platform_submission=true`, `no_email_sending=true`, `no_digital_signature=true`, `human_in_the_loop=true`, `token_owner=individual`.

## 2. Runner result

- Runner exit code: `0`
- Status: `PASS_EXACT_ATTACHMENT_EVIDENCE`
- `expected_document_count=7`
- `exact_document_count=7`
- `missing_names=[]`
- `duplicate_names=[]`
- `manifest_sha256=74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121`
- Exactly one new run directory was created by this top-level invocation.
- Archive entries listed by EIS include protocol/notification XML files in addition to the seven exact documents; only the seven exact document names are required and each occurred exactly once.

## 3. Independent exact-evidence verification

Verified directly from owner-only run state without trusting runner stdout:

- Retrieval/safety metadata: procurement_source `zakupki_gov_ru_getdocs_ip`; notice identity resolves only to `0344100006426000005`; `external_actions=false`; `no_platform_submission=true`; `no_email_sending=true`; `no_digital_signature=true`; `archive_downloaded=true`; `archive_extraction_complete=true`; `getdocs_status=completed`; `analysis_status=not_started`; `requested_analyze_after_download=false`.
- Exact source-listed set (NFC-normalized `original_name`): each of the seven expected document names occurs exactly once; none missing; none duplicated.
- File-system safety: stored names are relative, no `..`, no symlink components, resolved paths stay under the run input directory, files exist and are regular.
- Independent byte verification: per-file SHA-256 and sizes recomputed from bytes match the manifest `documents[]` and the declared metadata sizes for all seven exact files.
- Manifest-body integrity: `schema_version=p6.05-exact-attachment-evidence-v1`, `purpose=exact-tender-attachment-evidence`, `status=PASS_EXACT_ATTACHMENT_EVIDENCE`, `notice_number=0344100006426000005`, counts 7/7, `missing_names=[]`, `duplicate_names=[]`, seven document names in expected order. Canonical body bytes rebuilt independently (`json.dumps(..., ensure_ascii=False, sort_keys=True, separators=(",", ":"))`) hash to the recorded `manifest_sha256`, and `manifest_integrity_ref == sha256:<same hash>`; both equal the runner-reported `manifest_sha256`.
- Product-helper rebuild: `build_exact_attachment_evidence(metadata, input_dir=...)` reproduces the stored manifest byte-identically.
- Result: PASS.

## 4. External authority and boundaries

- External authority for the EIS chain preserved; no false `Native` substitution; no capability promotion; no Product Contract expansion; no CAP-002/CAP-003.
- No token/token metadata, `ref_id`, raw XML/SOAP, archive URL/query, absolute local paths, opaque Organization/Principal/run IDs, document contents, or PEM/certificate chain are recorded in this review or committed.
- Owner-only runtime artifacts (runs, archive, evidence, diagnostics) remain outside both repositories.

## 5. Outcome and next gate

- P6.05-L7 attempt #2: **PASS**. Real exact `7/7` exact-attachment evidence: **OBSERVED**.
- L7 proposed: `Complete / PASS`. L8 proposed: `Current / next` (L8 execution is NOT authorized by this task).
- P6.05 overall remains `Active / In Progress` until L8 closure.
- No retry performed after attempt #2; both repository worktrees clean.
