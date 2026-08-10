# P6.05-L2 — Reproducible Local Reference Runtime Start

Status: `Prepared / owner-operated Mac execution required for PASS`
Date: `2026-08-10`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operational environment: `Internal / local owner-operated runtime`
Production-readiness claim: `None`

## 1. Purpose

This runbook is the minimum reversible bootstrap for `P6.05-L2 — Reproducible Arvectum OS local checkout + reference runtime start`.

It does not introduce a new runtime architecture. The current Arvectum OS reference harness is already an in-process, standard-library Python implementation and requires no third-party package installation, container runtime, HTTP listener, database, broker or public ingress for this bounded step.

The Mac mini remains an operational environment for internal validation, not a platform contract or supported macOS deployment target.

## 2. Canonical boundary

The L2 start must preserve:

- canonical repository `arutyunoveth/arvectum-os`;
- branch `main` synchronized exactly to `origin/main` before execution;
- a clean working tree before synchronization and after the reference run;
- the existing in-process reference runtime under `reference/python`;
- no product/EIS invocation in L2;
- no credentials or secret material in source control or evidence;
- no public bind or ingress;
- no claim of Production, operational readiness, Stable/public compatibility or capability promotion.

No Accepted ADR is required for this bounded, replaceable, stdlib-only local start because it does not establish a durable cross-cutting technology choice or external contract.

## 3. L1 prerequisites carried forward

P6.05-L1 established on the selected owner-operated Mac mini:

- macOS on Apple Silicon `arm64`;
- Git available;
- `/opt/homebrew/bin/python3` CPython `3.14.6` available at observation;
- `python3 -m venv` available;
- the current reference suite passes on that interpreter family;
- Docker/Colima are not required for the in-process reference contour;
- no Arvectum OS network port is required;
- the selected clean checkout is under `<local-root>/arvectum-os`;
- runtime/evidence/configuration locations are outside the source-controlled checkout.

The EIS proxy/TLS constraint observed in L1 is deliberately out of scope for L2 and remains a later L3/L7 concern.

## 4. Reproducible start command

The L1 checkout may predate publication of this bootstrap. Therefore the first L2 invocation begins by safely acquiring the current canonical `main` before invoking the checked-in script:

```sh
cd <local-root>/arvectum-os
git fetch origin main
git merge --ff-only origin/main
sh reference/python/p6_05_l2_local_start.sh
```

The explicit `fetch + merge --ff-only` is only a bootstrap-acquisition step. It does not allow local history rewriting or conflict resolution. The checked-in L2 script then repeats canonical synchronization and exact `HEAD == origin/main` verification deliberately, making the execution idempotent and preserving read-after-write evidence.

Optional environment overrides are local-only and must not be committed:

```sh
ARVECTUM_LOCAL_ROOT=<local-root> \
PYTHON_BIN=/opt/homebrew/bin/python3 \
sh reference/python/p6_05_l2_local_start.sh
```

The script performs only these bounded actions:

1. verifies that `origin` is one of the accepted canonical GitHub HTTPS/SSH forms for `arutyunoveth/arvectum-os`;
2. requires branch `main` and a clean working tree;
3. fetches `origin/main` and fast-forwards local `main` only;
4. verifies exact `HEAD == origin/main`;
5. creates an isolated version-specific venv outside the source checkout;
6. performs no third-party dependency installation because the current harness is stdlib-only;
7. runs the existing reference runtime suite with Python bytecode writes disabled for that process tree so the validation itself does not create `__pycache__` / `.pyc` artifacts inside the source checkout:

```sh
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
```

8. verifies that the source checkout remains clean after the runtime suite;
9. stores a secret-safe local log and summary under `<local-root>/evidence/p6-05-l2/`;
10. records `external_actions=false`, `product_invoked=false`, `eis_invoked=false` and `public_ingress=false`.

Disabling bytecode writes is a local execution hygiene control only. It does not change reference runtime semantics, dependencies, persistence, public interfaces or architecture.

## 5. Expected PASS evidence

L2 may be marked `PASS` only after the command executes on the selected Mac mini and the resulting evidence demonstrates all of the following:

- `p6_05_l2_status=PASS`;
- branch is `main`;
- local `head_sha` exactly equals `origin_main_sha`;
- the isolated venv Python version is recorded;
- dependency mode is `stdlib-only; no third-party dependency installation`;
- runtime mode is `in-process reference harness`;
- the full reference suite result is `OK`;
- the observed test count is recorded from the actual local run;
- `working_tree_after_runtime=clean`;
- no product, EIS, public ingress or external action was invoked.

The test count must be recorded from the live Mac execution. It must not be copied from an earlier hosted or local observation.

## 6. Failure behavior

The bootstrap fails closed when:

- the checkout is not the canonical repository;
- the checkout is not on `main`;
- the working tree is dirty before synchronization;
- canonical `main` cannot be fetched or fast-forwarded;
- local `HEAD` does not equal `origin/main` after synchronization;
- Python or `venv` is unavailable;
- the reference suite fails;
- the reference suite leaves the source checkout dirty.

A failure remains evidence and must not be converted into `PASS`.

The script does not modify system proxy settings, EIS TLS policy, product configuration, secrets, external systems or platform canonical state.

## 7. Rollback / removal

The L2 bootstrap is removable without changing platform architecture:

- remove the version-specific venv under `<local-root>/runtime-data/venvs/`;
- remove generated L2 evidence under `<local-root>/evidence/p6-05-l2/` when retention is no longer required;
- recreate the source checkout from canonical Git history if needed.

No container, daemon, public listener, system service, database or durable platform dependency is installed by this runbook.

## 8. Canonical closure rule

Publishing this runbook and bootstrap script is preparation, not L2 completion.

`P6.05-L2` remains current until the selected owner-operated Mac mini executes the bootstrap and the actual local result is canonically recorded. Only then should the P6.05 local substream and canonical roadmap be synchronized to mark L2 complete and advance to `P6.05-L3`.
