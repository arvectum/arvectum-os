# P6.05-L3 — Multi-checkout Legacy EIS Secret Recovery

Status: `Prepared / owner-operated Mac execution required for PASS`
Date: `2026-08-10`
Owner: `ООО «Арвектум»`
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

## 3. Normal consistency rule and approved divergent-recovery exception

### 3.1 Normal multi-checkout consistency rule

Under normal multi-source recovery, all configured legacy copies must be equal.

When multiple verified local `ai-corporation` checkouts contain the EIS token key, choosing one checkout and migrating only that copy leaves reusable credentials in the remaining repo-local env files. That does not satisfy the intended L3 secrets boundary.

The recovery therefore treats the discovered legacy copies as a set:

1. inspect every explicitly supplied source env under owner-only permissions;
2. extract candidate secret values only in process memory;
3. require all configured source values to be byte-for-byte equal without printing or hashing them;
4. write one external owner-only destination, or safely reuse an already-created matching destination;
5. remove only the EIS token assignment from every supplied source that still contains it;
6. preserve unrelated env content;
7. retain only safe counts/status booleans as evidence.

If configured source values differ, the normal helper fails before creating a new destination or scrubbing any source.

### 3.2 Approved P6.05-L3 divergent-recovery exception

When owner-operated diagnostics on the fixed 7-source discovery manifest proved a 5+2 divergent secret distribution across legacy env files, the owner approved an explicit reconciliation decision (`DECISION-2026-08-14-P6-05-L3-DIVERGENT-EIS-SECRET-RECONCILIATION.md`).

ONLY the exact owner-approved fixed 7-source manifest may use this bounded exception, and only when the exact structural/value evidence matches:

- 7 source checkouts (`arvectum/ai-corporation`);
- 7 legacy env sources;
- 2 distinct secret equality classes;
- 5+2 class distribution;
- 4 `.env.local` sources;
- all 4 `.env.local` sources in the selected 5-source class;
- exact 2/4/1 local source ownership structure (2 manifest `ai-corporation`, 4 standalone, 1 owner-approved other local Git worktree);
- explicit owner authorization assertion (`OWNER_APPROVES_P6_05_L3_DOT_ENV_LOCAL_CLASS_RECONCILIATION`).

The canonical helper for this exception is `reference/python/p6_05_l3_reconcile_owner_selected_divergent_sources.py`.

This exception does not create a general secret conflict resolution rule.

## 4. Canonical migration helper

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

## 6. Baseline-aware discovery recovery

A discovered product checkout may already contain unrelated tracked local work. L3 does not own that work and must not erase, stash, reset, stage, commit or otherwise modify it merely to obtain a clean-tree precondition.

For an already-produced local-only discovery manifest, use:

```text
reference/python/p6_05_l3_recover_discovered_sources.py
```

Example:

```sh
python3 reference/python/p6_05_l3_recover_discovered_sources.py \
  --discovery-file "$ARVECTUM_LOCAL_ROOT/evidence/p6-05-l3/discovery-local-only.txt" \
  --destination "$ARVECTUM_LOCAL_ROOT/local-secrets/eis-soap-token" \
  --expected-checkout-count 7 \
  --expected-env-count 7
```

The bounded legacy filename scope intentionally matches the discovery procedure: `.env.local` and files whose basename ends exactly in `.env`, including `.env` itself and names such as `legacy.env`. This does **not** admit arbitrary configuration files or shell profiles. Names such as `.zshrc`, `.bash_profile`, `.env.production`, `config.txt` or `legacy.env.backup` fail closed.

The helper:

- verifies the discovery file and explicit expected counts;
- verifies each checkout's Git `origin` identifies `arutyunoveth/ai-corporation` without emitting the remote value;
- verifies every legacy env source uses the bounded filename scope, is untracked and maps unambiguously into a supplied checkout;
- rejects direct/parent env symlink sources;
- makes the env source owner-only before secret reliance;
- captures each checkout's `HEAD` and tracked `git status --porcelain=v1 --untracked-files=no` entirely in process memory;
- allows pre-existing tracked dirtiness;
- invokes the canonical multi-source migration helper;
- captures the same tracked state afterward and requires exact equality for every checkout;
- verifies no supplied legacy env still contains the EIS token key;
- emits only counts, booleans and safe failure codes.

Paths, filenames from tracked status, diffs, remote URLs, token values and token hashes are not emitted. A pre-existing dirty checkout therefore does not block L3 when its tracked state remains exactly unchanged. Any new tracked-state or `HEAD` change during migration fails closed.

## 7. Safe output

A successful seven-source recovery may emit safe state such as:

```text
p6_05_l3_discovered_source_recovery_status=PASS
source_checkout_count=7
source_env_count=7
source_remote_verified_count=7
source_env_untracked_count=7
tracked_dirty_before_count=1
tracked_state_unchanged=true
tracked_head_unchanged=true
source_envs_with_eis_key_remaining=0
preexisting_tracked_changes_modified=false
secret_values_printed=false
secret_values_hashed=false
secret_values_committed=false
product_invoked=false
eis_invoked=false
network_invoked=false
external_actions=false
p6_05_l3_secret_migration_status=PASS
...
```

The exact dirty-before count is descriptive evidence only. It is not a conformance failure. The required invariant is `tracked_state_unchanged=true` and `tracked_head_unchanged=true`.

## 8. Fail-closed conditions

Safe failure includes, without limitation:

- discovery-file absence, invalid encoding, symlink or excessive size;
- expected checkout/env count drift;
- unverified product remote;
- unsupported legacy source filename outside `.env.local` / `*.env`;
- ambiguous env-to-checkout mapping;
- tracked or symlinked legacy env source;
- source-pair count mismatch or duplicate source env path;
- missing, non-regular, oversized or broadly readable source env;
- duplicate or placeholder token assignment in a source;
- no token source when no destination exists;
- differing configured token values across sources;
- existing destination that is unsafe, invalid or does not match remaining source tokens;
- destination inside any supplied source checkout or the Arvectum OS checkout;
- incomplete source scrub after destination preservation;
- any product checkout `HEAD` or tracked status changing during migration;
- any supplied source still containing the EIS key after a migration reported PASS.

No failure output contains token values, hashes, checkout paths, tracked filenames/diffs or remote URLs.

## 9. Test evidence

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

`reference/python/tests/test_p6_05_l3_recover_discovered_sources.py` proves:

- seven-source recovery passes when one checkout has a pre-existing tracked modification and that state is preserved exactly;
- tracked legacy env files fail before migration;
- wrong repository remotes fail without emitting remote/path data;
- expected source-count drift fails closed;
- differing source secrets fail while preserving tracked baseline state;
- a newly introduced tracked change during migration is detected and fails closed.

`reference/python/tests/test_p6_05_l3_recover_env_filename_boundary.py` additionally proves that:

- `.env.local`, `.env` and bounded `*.env` filenames are accepted consistently with discovery;
- arbitrary shell/config filenames and near-miss suffixes remain rejected;
- a named `*.env` legacy source completes the same recovery path without exposing the synthetic secret.

All test credentials are synthetic and carry no external authority.

## 10. Closure rule

This recovery preparation does not complete L3 by itself.

L3 remains open until the owner-operated Mac mini runs the canonical discovery recovery/migration helper against the complete discovered source set, the canonical L3 preflight passes against the external config/secret boundary, and the bounded synthetic test suites pass. The Arvectum OS execution checkout must remain clean. Each discovered product checkout must preserve its exact pre-migration `HEAD` and tracked status; pre-existing tracked dirtiness is permitted but must not be modified by L3.

No product, EIS, TLS/proxy, network or external action is authorized by this recovery step. P6.05 remains open after L3 and only advances to L4 after canonical review of safe local PASS evidence.
