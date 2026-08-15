# P6.05-L7 attempt #1 — EIS TLS trust blocker

* Status: `Blocked / FAIL-CLOSED`
* Date: `2026-08-15`
* Owner: `ООО «Арвектум»`
* Task classification: `platform` with `product_contract` and `product_specific`
* Operational Environment: `Internal / local owner-operated runtime`
* Production-readiness claim: `None`
* Platform SHA (attempt #1): `3e2095c84c73168bc2ae3edfc704582a5d1ef3d6`
* Product SHA (attempt #1): `2aa3e6d1d53f70b4cb5c22c951bc5313c9b6bb38`

## 1. Attempt #1 facts

- Exactly one top-level execution of `scripts/p6_05_capture_real_attachment_evidence.py`.
- Notice `0344100006426000005`, law `44fz`, subsystem `PRIZ`, method `getDocsByReestrNumber`, `download_archive=True`, `analyze_after_download=False`.
- A read-only getDocsIP SOAP request was attempted against `int.zakupki.gov.ru`; TLS verification failed before any application response.
- Error class: `CERTIFICATE_VERIFY_FAILED` / `self-signed certificate in certificate chain` (OpenSSL `X509_V_ERR_SELF_SIGNED_CERT_IN_CHAIN`, code 19).
- Archive download: NO. Exact documents: `0/7`. Manifest: none. Product analysis: NO. `external_actions=false`.
- No L7 rerun; no L8 started. Both Git worktrees clean; live run state kept owner-only outside both repositories.

## 2. Active trust-policy summary (evidence-backed)

- No `ARVECTUM_ETP_TLS_*` configuration exists in the shell environment, repository `.env`/`.env.local`, or the external L3 configuration; the active trust policy therefore resolved to the product default.
- `policy_from_environment()` -> `enabled=False`, no host rules, no authorities; host `int.zakupki.gov.ru` matched: NO.
- Effective SSL context: `ssl.create_default_context()` (standard Python trust), `verify_mode=CERT_REQUIRED`, `check_hostname=True`, minimum TLS 1.2.
- Proxy bypass/`direct_connection`: not engaged (policy disabled); the connection still routed direct (no proxy) via the EIS client settings.
- The `route_mode=direct_for_eis` value in the SOAP runtime status is a settings-derived diagnostic label, not the policy-based route label; it did not change the direct connection or the TLS verification failure.

## 3. Root-cause disposition

- **Disposition: D — SYSTEM_TRUST_CHAIN_UNAVAILABLE** (the Python runtime trust store lacks the required national PKI root).
- Evidence:
  1. System-trust `openssl s_client` to `int.zakupki.gov.ru:443` (SNI, `-showcerts`, TLS 1.2) receives a complete chain — leaf `CN=*.zakupki.gov.ru` (O=ФЕДЕРАЛЬНОЕ КАЗНАЧЕЙСТВО) -> `CN=Russian Trusted Sub CA` -> `CN=Russian Trusted Root CA` (O=The Ministry of Digital Development and Communications) — and verifies `OK` against the macOS system trust (verify return 1 at all depths).
  2. A bare TLS-only handshake with the product Python 3.11 `ssl.create_default_context()` reproduces the exact L7 error (`CERTIFICATE_VERIFY_FAILED`, code 19) with no product code involved.
  3. A TLS-only handshake with `truststore.SSLContext(PROTOCOL_TLS_CLIENT)` (macOS system keychain, already used by the product for `authority: system`) succeeds, confirming the required root is present in the system keychain but absent from the Python default context.
- Leaf certificate (safe public metadata): subject `CN=*.zakupki.gov.ru`, issuer `CN=Russian Trusted Sub CA`, validity `2026-03-17` .. `2027-03-17`, SHA-256 fingerprint `3B76E9699D7D00CB2CA239EFB18CDE05B024010D5FA8DAF3192C31E235B714A4`.
- The presented server chain is complete and valid; this is not a server-side chain defect and not evidence of interception.
- Confidence: HIGH.

## 4. Governance level

- The existing product abstraction already supports an owner-operated ETP trust policy with `authority: system` (truststore) or `authority: file` with a pinned CA SHA-256, while preserving `CERT_REQUIRED`, hostname verification, and TLS >= 1.2.
- Remediation is therefore **product/operator configuration** within the existing abstraction: no Constitution/RFC/ADR/Product Contract/capability-contract change.
- If a reusable cross-product platform trust contract is later required, stop at the appropriate ADR/RFC gate.

## 5. Boundaries preserved

- No token read, printed, hashed, or persisted during the diagnostic; no HTTP/SOAP request and no archive download during the diagnostic (TLS-only handshake diagnostics only).
- No certificate verification weakened; no OS trust/keychain mutated; no CA material downloaded; no active trust policy mutated.
- External authority for the EIS chain preserved; no false `Native` substitution.
- P6.05 remains `Active / In Progress`; real `7/7` unobserved; L8 not started.

## 6. Remediation required (proposal, NOT executed)

Minimal proposed remediation for independent review (must not be applied in this task):

1. Create an owner-operated ETP trust policy (outside both Git worktrees) enabling the existing policy path for `.zakupki.gov.ru` hosts with `authority: system` (truststore), or `authority: file` with the Russian national root CA pinned by SHA-256 from an authoritative source.
2. Export `ARVECTUM_ETP_TLS_ENABLED=1` and `ARVECTUM_ETP_TLS_POLICY_PATH` only for the L7 process; preserve all L3 controls and the external owner-only token/configuration unchanged.
3. Re-run the platform L3 preflight to confirm controls unchanged; then execute a separately authorized one-shot P6.05-L7 retry.

Sequence: diagnosis -> independent review -> minimal remediation -> separately authorized one-shot L7 retry.
