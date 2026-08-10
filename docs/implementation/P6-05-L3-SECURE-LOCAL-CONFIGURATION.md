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

A previously working local installation may already contain the authorized EIS token in the product checkout's `.env` or `.env.local`. That historical state is a migration source only; it is not the desired L3 boundary.

Do not search for the token by value and do not print the matching env line. First locate the `ai-corporation` checkout by repository metadata/path only, then identify `.env.local` or `.env` by filename only.

The canonical migration helper is:

```text
reference/python/p6_05_l3_migrate_eis_secret.py
```

It requires three explicit paths:

- `--source-checkout-root` — verified local `ai-corporation` checkout;
- `--source-env` — the `.env.local` or `.env` file inside that checkout;
- `--destination` — `<local-root>/local-secrets/eis-soap-token` outside both checkouts.

Example invocation from the Arvectum OS checkout:

```sh
python3 reference/python/p6_05_l3_migrate_eis_secret.py \
  --source-checkout-root "$AI_CORPORATION_CHECKOUT" \
  --source-env "$AI_CORPORATION_CHECKOUT/.env.local" \
  --destination "$ARVECTUM_LOCAL_ROOT/local-secrets/eis-soap-token"
```

The helper:

- requires the legacy source env file itself to be owner-only before reading it;
- accepts exactly one `ZAKUPKI_GOV_RU_SOAP_TOKEN` assignment, including a shell-sourced `export` form or one quoted value;
- rejects missing, duplicate, placeholder or ambiguous secret state without echoing the value;
- creates the destination exclusively with owner-only mode and never overwrites an existing destination;
- refuses a destination inside either source-controlled checkout;
- after successfully creating the external destination, atomically removes only the token assignment from the legacy source env file while preserving all unrelated lines;
- creates no backup containing the secret;
- rolls back the newly created destination if the source env scrub cannot be completed;
- never prints or hashes the token;
- performs no product, EIS, network, canonical mutation or external action.

A successful migration emits only safe state such as:

```text
p6_05_l3_secret_migration_status=PASS
source_secret_detected=true
source_secret_removed=true
destination_created=true
destination_owner_only=true
secret.ZAKUPKI_GOV_RU_SOAP_TOKEN=configured
secret_values_printed=false
secret_values_hashed=false
backup_with_secret_created=false
product_invoked=false
eis_invoked=false
network_invoked=false
external_actions=false
```

After migration, both Arvectum OS and `ai-corporation` checkouts must still have clean tracked working trees. The presence of unrelated non-secret settings in the product `.env.local` is not itself L3 evidence; later P6.05 product connection must explicitly inject the selected L3 config/secret boundary rather than rely on repo-local secret storage.

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

- a legacy `.env.local` token can be migrated and scrubbed without appearing in output;
- quoted and shell-sourced `export` forms are supported;
- missing, duplicate and placeholder secret state fails closed;
- broad source-file permissions fail before secret reliance;
- a destination inside the product checkout is rejected;
- an existing destination is never overwritten.

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
