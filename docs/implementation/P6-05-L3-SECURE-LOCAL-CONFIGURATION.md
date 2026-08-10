# P6.05-L3 — Secure Local Configuration + Secrets Boundary

Status: `Prepared / owner-operated Mac execution required for PASS`
Date: `2026-08-10`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operational environment: `Internal / local owner-operated runtime`
Production-readiness claim: `None`

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

A previously working local installation may already contain the authorized EIS token in one or more product checkouts' `.env` or `.env.local` files. That historical state is a migration source only; it is not the desired L3 boundary.

Do not search for the token by value and do not print a matching env line. Locate `ai-corporation` checkouts by repository metadata/path only, then identify candidate `.env.local` or `.env` files by filename/key presence without emitting the value.

The canonical migration helper is:

```text
reference/python/p6_05_l3_migrate_eis_secret.py
```

It accepts one or more explicit source pairs plus one destination:

- repeated `--source-checkout-root` — verified local `ai-corporation` checkout;
- repeated `--source-env` — corresponding `.env.local` or `.env` file inside that checkout;
- `--destination` — `<local-root>/local-secrets/eis-soap-token` outside Arvectum OS and every supplied product checkout.

The number of source checkout and source env arguments must match. A single-source invocation remains valid. For multiple legacy copies, provide the complete discovered source set in one invocation.

Example multi-source invocation from the Arvectum OS checkout:

```sh
python3 reference/python/p6_05_l3_migrate_eis_secret.py \
  --source-checkout-root "$CHECKOUT_1" \
  --source-env "$ENV_1" \
  --source-checkout-root "$CHECKOUT_2" \
  --source-env "$ENV_2" \
  --destination "$ARVECTUM_LOCAL_ROOT/local-secrets/eis-soap-token"
```

The helper:

- requires every legacy source env file to be owner-only before reading it;
- accepts at most one `ZAKUPKI_GOV_RU_SOAP_TOKEN` assignment per source, including shell-sourced `export` form or one quoted value;
- treats a source with no token assignment as already scrubbed when a valid external destination already exists or another supplied source establishes the migration value;
- rejects duplicate, placeholder or malformed secret state without echoing the value;
- compares configured source values only in process memory and requires them all to be equal before creating a new destination or scrubbing any source;
- creates a new destination exclusively with owner-only mode when none exists;
- may reuse an already-existing owner-only destination only when every remaining supplied source token matches it in memory;
- never overwrites an existing destination;
- refuses a destination inside Arvectum OS or any supplied product checkout;
- removes only the token assignment from each supplied source that still contains it while preserving unrelated lines;
- creates no backup containing the secret;
- never prints or hashes the token;
- performs no product, EIS, network, canonical mutation or external action.

If a source rewrite fails after a valid destination has been created or reused, the helper preserves the destination, does not reintroduce the token into already-scrubbed sources, and returns `SOURCE_SCRUB_INCOMPLETE_DESTINATION_PRESERVED`. Re-running the same complete source set is the bounded recovery path after the local filesystem issue is corrected.

A successful multi-source migration emits only safe state such as:

```text
p6_05_l3_secret_migration_status=PASS
migration_scope=legacy_repo_local_eis_token_set_to_external_owner_only_file
source_count=7
sources_with_secret_before=7
sources_already_scrubbed_before=0
sources_scrubbed=7
destination_created=true
destination_reused=false
all_source_secrets_consistent=true
all_sources_scrubbed=true
destination_owner_only=true
secret.ZAKUPKI_GOV_RU_SOAP_TOKEN=configured
secret_values_printed=false
secret_values_hashed=false
secret_values_exported=false
secret_values_persisted_as_evidence=false
backup_with_secret_created=false
product_invoked=false
eis_invoked=false
network_invoked=false
external_actions=false
```

Counts may differ on an idempotent retry. Paths and secret values are not canonical evidence.

For the full multi-checkout recovery rationale and fail-closed semantics, see `P6-05-L3-MULTI-CHECKOUT-SECRET-RECOVERY.md`.

After migration, Arvectum OS and every supplied `ai-corporation` checkout must still have clean tracked working trees. The presence of unrelated non-secret settings in product `.env.local` files is not itself L3 evidence; later P6.05 product connection must explicitly inject the selected L3 config/secret boundary rather than rely on repo-local secret storage.

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

Failures identify only a safe code and, where useful, the configuration key name. They do not echo the rejected value.

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

All test tokens are synthetic and have no external authority or credential value.

## 10. Owner-operated Mac execution and evidence

Publishing the runbook/preflight/tests is preparation, not L3 completion.

L3 may be marked `PASS` only after the selected owner-operated Mac mini executes the canonical migration helper where required, then executes the canonical preflight against the actual external local configuration and authorized local token file, plus bounded synthetic negative-path checks, while preserving clean tracked working trees.

The retained L3 evidence must contain only safe migration/preflight summaries and source-control state. Do not retain raw config, raw token content, environment dumps, shell traces, token hashes or legacy secret-bearing source-env contents as canonical evidence.

The actual EIS TLS/proxy reachability observed as constrained in L1 is not converted into a PASS by this configuration check. Live reachability remains subject to later authorized execution and must fail closed if the verified path is unavailable.

## 11. Rollback / removal

The L3 mechanism is removable without changing Arvectum OS architecture:

- remove the bounded non-secret local config when no longer needed;
- remove/rotate/revoke the local EIS credential according to the credential owner's existing authority and source-system process;
- remove generated L3 safe evidence according to applicable retention;
- remove the checked-in preflight/runbook/tests through normal source-control change if the local mechanism is later replaced.

Removal of local files must not be represented as revocation at the authoritative EIS source. Credential revocation is a distinct external-authority operation.

## 12. Canonical closure rule

`P6.05-L3` remains the current canonical action until actual owner-operated PASS evidence is reviewed and recorded. Only then should the P6.05 substream and roadmaps be synchronized to mark L3 complete and advance to `P6.05-L4 — Internal Organization + operator bootstrap`.

Successful L3 proves only the bounded local configuration/secrets boundary. It does not close P6.05, establish Production readiness, authorize product/EIS execution, promote a capability or create a Stable/public contract.
