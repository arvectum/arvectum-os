# P6.05-L2 — Local Reference Runtime Start Evidence

Status: `Complete / PASS`
Date: `2026-08-10`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operational environment: `Internal / local owner-operated runtime`
Production-readiness claim: `None`

## 1. Scope

This review records the actual owner-operated Mac mini execution evidence for `P6.05-L2 — Reproducible Arvectum OS local checkout + reference runtime start`.

It proves only that the bounded Arvectum OS reference runtime can be reproduced from canonical `main` in the selected internal environment while preserving a clean source checkout and the declared no-product/no-EIS/no-public-ingress boundary.

It does not establish Production readiness, a supported macOS deployment target, a Stable/public runtime contract, a persistent deployment topology, Product Contract execution, capability lifecycle promotion or completion of P6.05.

## 2. Canonical baseline

The successful run used:

- canonical repository: `arutyunoveth/arvectum-os`;
- branch: `main`;
- local `HEAD`: `fb61889633b11875dc5e1cf92771a159024a5695`;
- `origin/main`: `fb61889633b11875dc5e1cf92771a159024a5695`;
- working tree before execution: clean;
- source checkout reconstructed as a fresh canonical clone under `<local-root>/arvectum-os-l2-retry`;
- runtime/evidence locations remained outside the source-controlled checkout.

The canonical L2 bootstrap at this SHA includes the remediation merged through PR `#85`, which suppresses Python bytecode writes during the reference suite rather than hiding generated cache artifacts through ignore rules.

## 3. Runtime evidence

Observed interpreter and environment:

- Python binary selected by the operator: `/opt/homebrew/bin/python3`;
- CPython: `3.14.6`;
- platform reported by the isolated venv: `macOS-26.6.1-arm64-arm-64bit-Mach-O`;
- dependency mode: `stdlib-only; no third-party dependency installation`;
- runtime mode: `in-process reference harness`.

Executed bootstrap:

```sh
ARVECTUM_LOCAL_ROOT=<local-root> \
PYTHON_BIN=/opt/homebrew/bin/python3 \
sh reference/python/p6_05_l2_local_start.sh
```

Recorded runtime command inside the generated evidence:

```text
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
```

Observed result:

```text
Ran 717 tests in 0.980s
OK
```

Post-run state:

- working tree: clean;
- `__pycache__` / `.pyc` artifacts under `reference/python`: none;
- local `HEAD == origin/main`: yes.

## 4. Generated local evidence

The successful bootstrap created secret-safe local evidence under:

`<local-root>/evidence/p6-05-l2/20260810T054403Z-fb61889633b1/`

The generated `summary.txt` recorded:

```text
p6_05_l2_status=PASS
operational_environment=Internal / local owner-operated runtime
production_readiness_claim=None
canonical_repository=arutyunoveth/arvectum-os
branch=main
head_sha=fb61889633b11875dc5e1cf92771a159024a5695
origin_main_sha=fb61889633b11875dc5e1cf92771a159024a5695
python_version=3.14.6
platform=macOS-26.6.1-arm64-arm-64bit-Mach-O
dependency_mode=stdlib-only; no third-party dependency installation
runtime_mode=in-process reference harness
runtime_command=PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
runtime_result=OK
runtime_test_count=Ran 717 tests in 0.980s
working_tree_after_runtime=clean
external_actions=false
public_ingress=false
product_invoked=false
eis_invoked=false
log_file=<local-root>/evidence/p6-05-l2/20260810T054403Z-fb61889633b1/reference-runtime.log
```

No secret value, token, private key, certificate content, cookie, proxy credential or `.env` content was read into the reported evidence.

## 5. Fail-closed history and remediation

The first fresh-checkout L2 execution on canonical `7ff47be8184e14f712a2168e69879eddaeffe4ab` passed all `717` tests but correctly returned `FAIL` because the test process generated untracked Python `__pycache__/` directories, making `working_tree_after_runtime=dirty`.

That failure was preserved as truthful operational evidence rather than converted into PASS.

The minimum bounded remediation was merged through PR `#85` as canonical commit `fb61889633b11875dc5e1cf92771a159024a5695`:

- Python bytecode writes are disabled only for the reference-suite process tree;
- the strict clean-before/clean-after gate remains unchanged;
- no `.gitignore` workaround hides generated files;
- no new dependency, persistence mechanism, service, public interface or architecture decision was introduced.

Hosted `Reference Python CI #281` passed on the remediation head before merge.

## 6. Security and boundary evidence

The successful L2 run recorded:

- `external_actions=false`;
- `product_invoked=false`;
- `eis_invoked=false`;
- `public_ingress=false`;
- no secret material accessed or printed;
- no repository changes made by the runtime.

The run therefore remained inside the declared internal/local bounded reference-runtime scope.

## 7. Dogfooding friction

Observed setup/runtime friction:

1. the earlier L1-selected checkout had drifted from the required L2 execution state and contained generated cache files, so a fresh canonical checkout was safer than destructive cleanup;
2. the first fresh L2 run exposed that the canonical reference-suite invocation itself wrote Python cache artifacts into the checkout;
3. the fail-closed clean-state gate correctly prevented that run from being represented as PASS;
4. the remediation was small and reversible: suppress bytecode writes for the validation process tree while preserving the strict clean-state assertion.

These observations are operational evidence. They do not establish a new platform capability, deployment topology or product requirement.

## 8. Exit-criteria assessment

- canonical repository and `main` used: PASS;
- local `HEAD == origin/main`: PASS;
- reproducible isolated Python environment created outside checkout: PASS;
- third-party dependency installation required: no;
- reference runtime suite executed: PASS;
- observed suite result `717/717`, `OK`: PASS;
- source checkout clean after execution: PASS;
- generated Python cache artifacts in source checkout: none;
- product/EIS/public-ingress/external actions: none;
- secret exposure: none observed.

## 9. Disposition

`P6.05-L2: Complete / PASS`

The successful local start is internal validation evidence only. It does not close P6.05 and does not change any capability, Product Contract, conformance or operational-readiness lifecycle.

`Next eligible action: P6.05-L3 — Secure local configuration + secrets boundary.`