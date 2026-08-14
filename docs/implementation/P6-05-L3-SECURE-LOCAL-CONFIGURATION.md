# P6.05-L3 — Secure Local Configuration + Secrets Boundary

Status: `Complete / owner-operated PASS recorded`
Date: `2026-08-10`
Updated: `2026-08-14`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operational environment: `Internal / local owner-operated runtime`
Production-readiness claim: `None`
Evidence review: [`docs/reviews/P6-05-L3-secure-local-configuration-secrets-boundary.md`](../reviews/P6-05-L3-secure-local-configuration-secrets-boundary.md)

## 1. Purpose

This runbook establishes the minimum reversible local configuration/secrets boundary required by `P6.05-L3` before the later Organization/operator bootstrap, product connection and real EIS evidence run.

The exit condition is intentionally narrow:

- configuration required by the selected workflow is outside source-controlled repository state;
- the reusable EIS credential is physically separated from non-secret configuration;
- the credential can be detected as configured without printing, hashing, persisting into evidence or committing its value;
- local file/directory permissions are owner-only;
- unsafe or incomplete states fail closed;
- no product, EIS, network, canonical mutation or external action occurs in L3.

This is not a general Arvectum OS secret-management architecture, production credential store, IAM topology, deployment contract or macOS support commitment.

## 2. Canonical and product basis

The relevant binding architecture is:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 `1.0.0` — `Accepted`;
- RFC-0003 `1.0.0` — `Accepted`: reusable secrets must use sensitivity-appropriate controls and must not be logged, placed in ordinary canonical payloads/portable exports or model prompts; least privilege and fail-closed behavior apply;
- RFC-0004 `1.0.0` — `Accepted`: product/platform interaction must not weaken RFC-0003 and Product Contract registration does not itself grant authority;
- RFC-0005 `1.0.0` — `Accepted`: L3 creates no consequential execution or canonical mutation;
- RFC-0006 `1.0.0` — `Accepted`: operational telemetry is non-canonical by default and remains subject to RFC-0003 minimization/secret rules.

No Accepted ADR currently governs this bounded local file mechanism, and no new ADR/RFC is required because the mechanism is local, reversible, non-public, non-production and does not establish a cross-cutting technology contract.

The selected product contour is the already-merged P6.05 `ai-corporation` runner. Its current settings implementation accepts `ZAKUPKI_GOV_RU_SOAP_TOKEN` from the process environment and seeds repository-local `.env` / `.env.local` only as a fallback. Therefore the later product connection can inject the token into the process environment without storing the token in the product checkout. L3 only proves the local boundary; it does not perform that later injection or invoke the product.

## 3. Selected local boundary

Use two separate local locations outside every source-controlled checkout:

```text
<local-root>/local-config/p6-05-l3.env
<local-root>/local-secrets/eis-soap-token
```

Required filesystem controls for this bounded internal contour:

- `<local-root>/local-config/` — owner-only directory (`0700`);
- `<local-root>/local-secrets/` — owner-only directory (`0700`);
- `p6-05-l3.env` — owner-only file (`0600` or stricter);
- `eis-soap-token` — owner-only file (`0600` or stricter);
- neither file may be a symlink;
- neither file may resolve inside the Arvectum OS checkout;
- the secret value MUST NOT appear in `p6-05-l3.env`.

For the current owner-operated internal validation, filesystem access control is the bounded local protection mechanism. This does not pre-select the secret-management technology for Production or customer environments.

## 4. Non-secret configuration

`<local-root>/local-config/p6-05-l3.env` contains only the explicit controls needed by the already-selected read-only EIS/getDocsIP contour:

```dotenv
ZAKUPKI_GOV_RU_SOAP_ENABLED=1
ZAKUPKI_GOV_RU_SOAP_TOKEN_OWNER=individual
ZAKUPKI_GOV_RU_SOAP_DISABLE_PROXY_FOR_EIS=1
ZAKUPKI_GOV_RU_SOAP_REQUIRE_DIRECT_RU_ROUTE=1
ZAKUPKI_GOV_RU_SOAP_TRUST_ENV_PROXY=0
ZAKUPKI_GOV_RU_SOAP_DEBUG=0
```

The L3 preflight accepts no other keys in this file. In particular, `ZAKUPKI_GOV_RU_SOAP_TOKEN` is explicitly rejected from the non-secret configuration.

The network/proxy controls are configuration assertions only in L3. The preflight does not contact EIS, modify the system PAC/proxy, bypass TLS verification or claim that the later live network path succeeds.

## 5. Secret file

`<local-root>/local-secrets/eis-soap-token` contains only the existing authorized EIS token value and a trailing newline if desired.

The L3 preflight:

- reads the value only long enough to determine that it is non-empty and not a known placeholder;
- does not print the value;
- does not hash the value;
- does not copy it into evidence;
- does not export it to a child process;
- does not contact EIS;
- does not retain it in canonical state.

Do not paste the token into project chat, issue/PR text, canonical evidence or source-controlled configuration.

## 6. Legacy repo-local secret migration

A previously working local installation may already contain the authorized EIS token in one or more product checkouts' legacy env files. For the bounded L3 discovery/recovery contour, eligible source filenames are `.env.local` and files whose basename ends exactly in `.env`, including `.env` itself and names such as `legacy.env`. That historical state is a migration source only; it is not the desired L3 boundary.

This filename scope intentionally matches the local discovery procedure. It does not admit arbitrary configuration files or shell profiles. Names such as `.zshrc`, `.bash_profile`, `.env.production`, `config.txt` and `legacy.env.backup` remain outside the recovery scope and fail closed.

Do not search for the token by value and do not print a matching env line. Locate `ai-corporation` checkouts by repository metadata/path only, then identify candidate `.env.local` / `*.env` sources by filename and key presence without emitting the value.

### 6.1 Normal multi-source migration

Under normal multi-source recovery where all discovered legacy copies contain identical secret values, the canonical migration helper is:

```text
reference/python/p6_05_l3_migrate_eis_secret.py
```

It requires all configured source values to be byte-for-byte equal in memory before creating a new destination or scrubbing any source.

### 6.2 Approved P6.05-L3 divergent-recovery exception

When owner-operated diagnostics on the fixed 7-source discovery manifest proved a 5+2 divergent secret distribution across legacy env files, the owner approved an explicit reconciliation decision (`DECISION-2026-08-14-P6-05-L3-DIVERGENT-EIS-SECRET-RECONCILIATION.md`).

For this exact fixed 7-source manifest, the canonical reconciliation helper is:

```text
reference/python/p6_05_l3_reconcile_owner_selected_divergent_sources.py
```

Invocation from the Arvectum OS execution checkout:

```sh
python3 reference/python/p6_05_l3_reconcile_owner_selected_divergent_sources.py \
  --discovery-file "$ARVECTUM_LOCAL_ROOT/evidence/p6-05-l3/discovery-local-only.txt" \
  --destination "$ARVECTUM_LOCAL_ROOT/local-secrets/eis-soap-token" \
  --expected-checkout-count 7 \
  --expected-env-count 7 \
  --owner-authorization OWNER_APPROVES_P6_05_L3_DOT_ENV_LOCAL_CLASS_RECONCILIATION
```

The helper:

- validates the 2/4/1 local source ownership structure (2 manifest `arvectum/ai-corporation` checkouts, 4 standalone sources, 1 owner-approved other local Git worktree);
- verifies that each manifest checkout remote matches `arvectum/ai-corporation` and that all legacy envs are untracked;
- captures in-memory Git snapshots of all 8 involved repositories (7 manifest checkouts + 1 other local Git worktree);
- classifies the 7 configured secret values in memory using constant-time equality;
- strictly enforces the owner-approved 5+2 distribution where all 4 `.env.local` sources belong to the 5-source equality class;
- establishes the 5-source selected credential at the external owner-only destination;
- scrubs the `ZAKUPKI_GOV_RU_SOAP_TOKEN` assignment from all 7 legacy sources;
- treats the 2 non-selected values as stale local copies without persisting or copying them anywhere;
- verifies that all 8 repository HEADs and tracked states remain exactly unchanged across reconciliation;
- never prints, hashes, encodes, or persists secret values.

This exception applies exclusively to the fixed P6.05-L3 discovery manifest under explicit owner authorization and does not establish a general secret conflict resolution rule.

## 7. Checked-in preflight

The canonical helper is:

```text
reference/python/p6_05_l3_secure_local_config.py
```

Invocation from the Arvectum OS checkout:

```sh
python3 reference/python/p6_05_l3_secure_local_config.py \
  --config "$ARVECTUM_LOCAL_ROOT/local-config/p6-05-l3.env" \
  --eis-token-file "$ARVECTUM_LOCAL_ROOT/local-secrets/eis-soap-token"
```

The helper is standard-library only and performs no network or product action.

Expected PASS output contains only safe state such as:

```text
p6_05_l3_status=PASS
configuration_source=external_nonsecret_local_file
secret_source=separate_external_owner_only_file
config_outside_source_control=true
secret_outside_source_control=true
secret.ZAKUPKI_GOV_RU_SOAP_TOKEN=configured
secret_values_printed=false
secret_values_hashed=false
secret_values_persisted_by_preflight=false
product_invoked=false
eis_invoked=false
network_invoked=false
external_actions=false
```

The output MUST NOT contain the token value or token-file contents.

## 8. Fail-closed conditions

The preflight returns non-zero and a safe failure code when any material boundary condition is not proven, including:

- configuration or secret file is missing;
- either file resolves inside the source checkout;
- either direct file path is a symlink;
- containing local configuration/secret directory is not owner-only;
- file permissions permit group/other access;
- non-secret config contains the EIS token;
- non-secret config contains an undeclared key;
- a required control is missing, malformed or differs from the selected safe contour;
- token value is empty or a known placeholder;
- local file is too large or not a regular UTF-8 file.

Discovery-driven recovery additionally fails closed if expected source counts drift, a candidate remote is not the declared `ai-corporation` repository, a legacy source filename falls outside `.env.local` / `*.env`, a legacy env is tracked or symlinked, env-to-checkout mapping is ambiguous, the canonical migration fails, any checkout HEAD or tracked state changes during migration, or any supplied legacy env still contains the EIS key afterward.

Failures identify only a safe code and, where useful, the configuration key name. They do not echo rejected values, local paths, tracked filenames or diffs.

## 9. Test evidence prepared in repository

`reference/python/tests/test_p6_05_l3_secure_local_config.py` proves with synthetic values that:

- separate owner-only config + secret files pass;
- the token is absent from diagnostics;
- a token placed in the non-secret file fails closed without echoing it;
- a placeholder token fails closed without echoing it;
- broad secret-file permissions fail closed;
- configuration inside the source checkout fails closed before reliance;
- unsafe control values fail without echoing the value;
- undeclared config keys are rejected;
- secret symlinks are rejected.

`reference/python/tests/test_p6_05_l3_migrate_eis_secret.py` additionally proves with synthetic values that:

- seven matching legacy repo-local copies migrate to one destination and all supplied copies are scrubbed;
- differing source values fail before a new destination or source mutation;
- a matching existing destination is reused without overwrite;
- a mismatching existing destination fails closed without overwrite;
- complete and partial retry paths are idempotent and scrub only remaining matching copies;
- quoted and shell-sourced `export` forms are supported;
- absent, duplicate and placeholder secret state fails closed where no valid destination/reference exists;
- broad source-file permissions fail before secret reliance;
- a destination inside any supplied product checkout is rejected;
- duplicate source env paths are rejected;
- secret values never appear in safe output.

`reference/python/tests/test_p6_05_l3_recover_discovered_sources.py` additionally proves that:

- the discovered seven-source recovery succeeds with a pre-existing tracked modification when that tracked state remains exactly unchanged;
- tracked legacy env files and wrong remotes fail before migration;
- source-count drift fails closed;
- differing secrets preserve the pre-existing tracked baseline and remain unmodified;
- a new tracked change during migration is detected and fails closed;
- local paths, remote values and synthetic secrets do not appear in safe output.

`reference/python/tests/test_p6_05_l3_recover_env_filename_boundary.py` proves the discovery/recovery filename alignment:

- `.env.local`, `.env` and bounded `*.env` filenames are accepted;
- arbitrary shell/config filenames and suffix near-misses remain rejected;
- a named `*.env` source runs through the same recovery/migration path without secret output.

All test tokens are synthetic and have no external authority or credential value.

## 10. Owner-operated Mac execution and evidence

Publishing the runbook/preflight/tests is preparation, not L3 completion.

L3 may be marked `PASS` only after the selected owner-operated Mac mini executes the canonical migration/recovery helper where required, then executes the canonical preflight against the actual external local configuration and authorized local token file, plus bounded synthetic negative-path checks. The Arvectum OS tracked working tree must be clean for the canonical execution checkout. For discovered legacy product checkouts, pre-existing tracked changes may remain, but their `HEAD` and tracked status must be proven unchanged across the migration; L3 must not create, remove, stage, commit, reset or otherwise alter those tracked changes.

The retained L3 evidence must contain only safe migration/preflight summaries and source-control state booleans/counts. Do not retain raw config, raw token content, environment dumps, shell traces, token hashes, checkout paths, tracked filenames/diffs or legacy secret-bearing source-env contents as canonical evidence.

The actual EIS TLS/proxy reachability observed as constrained in L1 is not converted into a PASS by this configuration check. Live reachability remains subject to later authorized execution and must fail closed if the verified path is unavailable.

## 11. Rollback / removal

The L3 mechanism is removable without changing Arvectum OS architecture:

- remove the bounded non-secret local config when no longer needed;
- remove/rotate/revoke the local EIS credential according to the credential owner's existing authority and source-system process;
- remove generated L3 safe evidence according to applicable retention;
- remove the checked-in preflight/runbook/tests through normal source-control change if the local mechanism is later replaced.

Removal of local files must not be represented as revocation at the authoritative EIS source. Credential revocation is a distinct external-authority operation.

## 12. Canonical closure

`P6.05-L3` owner-operated execution is complete and verified as `PASS`. The canonical evidence review is recorded in [`P6-05-L3-secure-local-configuration-secrets-boundary.md`](../reviews/P6-05-L3-secure-local-configuration-secrets-boundary.md).

Successful L3 proves the bounded local configuration/secrets boundary. The P6.05 substream advances to `P6.05-L4 — Internal Organization + operator bootstrap`. P6.05 overall remains open until real `7/7` attachment evidence is obtained.
