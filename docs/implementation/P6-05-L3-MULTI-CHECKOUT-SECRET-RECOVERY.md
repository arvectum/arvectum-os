# P6.05-L3 — Multi-checkout Legacy EIS Secret Recovery

Status: `Prepared / owner-operated Mac execution required for PASS`
Date: `2026-08-10`
Owner: `ООО «Арвектум»
Task classification: `platform`
Operational environment: `Internal / local owner-operated runtime`
Production-readiness claim: `None`

## 1. Purpose

This note refines the legacy-secret migration procedure in `P6-05-L3-SECURE-LOCAL-CONFIGURATION.md` for the bounded case where local discovery finds more than one `ai-corporation` checkout containing the same EIS credential key.

The L3 exit condition is unchanged. The goal is one external owner-only secret file and no remaining discovered repo-local copies of `ZAKUPKI_GOV_RU_SOAP_TOKEN` in the explicitly supplied legacy source env files.

This note does not create a general secret-management architecture, credential-rotation policy, Production topology, product invocation, EIS authorization or external action.

## 2. Canonical basis

The applicable authority remains:

- Constitution `1.2.0` — `Ratified`;
- RFC-0001 `1.0.0` — `Accepted`;
- RFC-0003 `1.0.0` — `Accepted`, including sensitivity-appropriate reusable-secret handling, minimization, least privilege and fail-closed behavior;
- RFC-0004 `1.0.0` — `Accepted`, without weakening RFC-0003 at the product/platform boundary;
- RFC-0005 `1.0.0` — `Accepted`; no consequential execution or canonical mutation occurs here;
- RFC-0006 `1.0.0` — `Accepted`; retained operational evidence remains secret-minimized and non-canonical by default.

No Accepted ADR governs this local reversible recovery mechanism. No new RFC/ADR is required because the change is bounded, local, reversible, non-public and does not establish a cross-cutting platform technology contract.

## 3. Why selecting one checkout is insufficient

When multiple verified local `ai-corporation` checkouts contain the EIS token key, choosing one checkout and migrating only that copy leaves reusable credentials in the remaining repo-local env files. That does not satisfy the intended L3 secrets boundary.

The recovery therefore treats the discovered legacy copies as a set:

1. inspect every explicitly supplied source env under owner-only permissions;
2. extract candidate secret values only in process memory;
3. require all configured source values to be byte-for-byte equal without printing or hashing them;
4. write one external owner-only destination, or safely reuse an already-created matching destination;
5. remove only the EIS token assignment from every supplied source that still contains it;
6. preserve unrelated env content;
7. retain only safe counts/status booleans as evidence.

If configured source values differ, the helper fails before creating a new destination or scrubbing any source.

## 4. Canonical helper

`reference/python/p6_05_l3_migrate_eis_secret.py` accepts repeated source pairs:

```sh
python3 reference/python/p6_05_l3_migrate_eis_secret.py \
  --source-checkout-root "$CHECKOUT_1" \
  --source-env "$ENV_1" \
  --source-checkout-root "$CHECKOUT_2" \
  --source-env "$ENV_2" \
  --destination "$ARVECTUM_LOCAL_ROOT/local-secrets/eis-soap-token"
```

The number of `--source-checkout-root` and `--source-env` arguments must match. Duplicate source env paths are rejected.

Every source env must:

- resolve inside its declared checkout;
- be a regular non-symlink file;
- be no larger than the bounded local-file limit;
- be owner-only before the helper reads it.

The destination must:

- be outside Arvectum OS and every supplied product checkout;
- have an owner-only parent directory;
- be a regular owner-only file if it already exists.

## 5. Consistency and retry semantics

If the destination does not yet exist, at least one supplied source must contain a configured non-placeholder EIS token. All supplied sources that contain the token must agree in memory before the helper writes anything.

If the destination already exists, the helper may reuse it only when every remaining supplied source token matches the existing destination in memory. The destination is never overwritten.

Sources that no longer contain the token are treated as already scrubbed. This makes retry safe after a prior successful run or after a partial filesystem interruption.

If a source rewrite fails after the destination exists, the helper preserves the destination and reports `SOURCE_SCRUB_INCOMPLETE_DESTINATION_PRESERVED`. It does not reintroduce the secret into already-scrubbed sources and does not create a secret-bearing backup. Re-running the same complete source set is the recovery path after the local filesystem issue is corrected.

## 6. Safe output

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

Counts may differ on idempotent retry. Paths and secret values are not part of canonical evidence.

## 7. Fail-closed conditions

Safe failure includes, without limitation:

- source-pair count mismatch;
- duplicate source env path;
- source outside its declared checkout;
- missing, non-regular, symlinked, oversized or broadly readable source env;
- duplicate or placeholder token assignment in a source;
- no token source when no destination exists;
- differing configured token values across sources;
- existing destination that is unsafe, invalid or does not match remaining source tokens;
- destination inside any supplied source checkout or the Arvectum OS checkout;
- incomplete source scrub after destination preservation.

No failure output contains token values or hashes.

## 8. Test evidence

`reference/python/tests/test_p6_05_l3_migrate_eis_secret.py` uses synthetic credentials to prove:

- seven matching legacy copies migrate to one destination and all seven are scrubbed;
- differing source values fail before destination creation or source mutation;
- a matching existing destination is reused without overwrite;
- a mismatching existing destination fails closed without overwrite;
- retry after complete scrub is idempotent;
- retry with some already-scrubbed sources removes only the remaining matching copies;
- quoted and shell `export` forms remain supported;
- duplicate keys, placeholder values, broad permissions, duplicate source paths and unsafe destination placement fail closed;
- secret values never appear in safe output.

All test credentials are synthetic and carry no external authority.

## 9. Closure rule

This recovery preparation does not complete L3 by itself.

L3 remains open until the owner-operated Mac mini runs the canonical helper against the complete discovered source set, the canonical L3 preflight passes against the external config/secret boundary, the bounded synthetic test suites pass, and tracked working trees remain clean.

No product, EIS, TLS/proxy, network or external action is authorized by this recovery step. P6.05 remains open after L3 and only advances to L4 after canonical review of safe local PASS evidence.
