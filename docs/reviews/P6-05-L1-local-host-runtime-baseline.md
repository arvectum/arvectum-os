# P6.05-L1 — Local Host / Runtime Baseline

Status: `Complete / PASS`
Date: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operational environment: `Internal / local owner-operated runtime`
Production-readiness claim: `None`

## 1. Scope

This is a bounded, secret-safe inventory of the current owner-operated Mac mini. It establishes prerequisites and reversible local locations for the current contour only. It neither starts a runtime nor selects a deployment, storage, container, network, or public-interface architecture.

## 2. Canonical baseline

- Constitution `1.2.0` — `Ratified`.
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`.
- No Accepted ADR exists in the canonical ADR location; historical ADR-named review artifacts are not ADR decisions.
- Roadmap `2.51.1`; P6.05 local substream `0.1.1`.
- Canonical `main` was fetched read-only and is at `743563839f257045ec025541f2a9b3926756bebc` with no local divergence.

## 3. Host

- macOS `26.6.1` (build `25G76`); timezone `MSK` (`+0300`).
- Apple Silicon `arm64`, model class `Mac16,11`; 12 logical CPUs and 24 GiB physical RAM.
- Workspace volume: APFS on `/System/Volumes/Data`, with 256 GiB available at observation.
- Rosetta service was detected (informational only).
- The intended local work-data location passed a create/read/remove probe under the normal local user; no ownership or permission change was needed.

## 4. Runtime / tooling

| Item | Observed | Required for current bounded contour | Disposition |
| ---- | -------- | ------------------------------------ | ----------- |
| Git | `2.55.0` | Yes | Available. |
| Python | `/opt/homebrew/bin/python3`, CPython `3.14.6` | Yes | Reference suite passed on this host (717 tests); hosted CI's 3.12 baseline is therefore not a blocker. |
| `pip` command | Not on `PATH`; `python3 -m pip` is `26.1.2` | Not demonstrated as required by the checked-in reference harness | Available through the interpreter; record for L2 only if a reproducible dependency installation needs it. |
| `venv` | Available through `python3 -m venv` | Potentially for L2 isolation | Available; no venv was created in L1. |
| Homebrew | `6.0.15` | No | Inventory only. |
| Docker / Colima | Docker `29.6.2`; Colima `0.10.3` | No | Inventory only; no container runtime is selected or required. |
| Podman | Not installed | No | No action required. |
| `make`, `curl`, `openssl` | Available | `make`/`curl`/`openssl` are not required by the in-process reference suite | Inventory only. |

The current Arvectum OS reference harness is a standard-library Python, in-process runtime (`python -m unittest discover -s tests -v`). It contains no checked-in package metadata or dependency manifest and exposes no required HTTP listener. The readiness baseline permits in-process composition; a container runtime or network port is not an L2 prerequisite.

## 5. Repository locations

| Repository | Local location | Branch / HEAD | Working tree | L2 disposition |
| ---------- | -------------- | ------------- | ------------ | -------------- |
| `arvectum-os` | `<local-root>/arvectum-os` | `main` / `743563839f257045ec025541f2a9b3926756bebc` | Clean | Safe clean canonical checkout for L2. |
| `ai-corporation` | existing owner workspace (outside `<local-root>`) | `fix/arv001-controlled-live-adapter` / `80832ef0638dac5d20d2bbe80d276bf12149d2d8` | Clean; tracks its origin branch | Inventory only; do not integrate in L1. |

The initially supplied `Arvectum-OS` directory is an unrelated empty Git repository with no commits or remote, so it was not modified. A separate clean clone was required to access canonical `main` without changing that directory. Other discovered `ai-corporation` copies are not selected: one `main` checkout is 216 commits behind its origin and one is a context dump.

## 6. Local data / configuration / evidence locations

The reversible local root is represented here as `<local-root>` rather than as a machine-specific contract:

- repositories: `<local-root>/arvectum-os` and the existing product checkout;
- runtime data: `<local-root>/runtime-data`;
- future exact-byte evidence and manifests: `<local-root>/evidence`;
- temporary files: `<local-root>/tmp`;
- future local-only configuration: `<local-root>/local-config`.

These locations are outside the source-controlled checkout. No secret file was created or copied in L1.

## 7. Network / proxy constraints

- GitHub read/fetch access passes over HTTPS; canonical `main` fetch reported no divergence.
- System proxy auto-configuration is enabled. GitHub access works through the active network path.
- DNS resolves `zakupki.gov.ru` and `int.zakupki.gov.ru`, but credential-free HTTPS connection attempts through the active proxy timed out. This is an observed EIS-network constraint, not a reason to bypass, change, or disable the proxy in L1.
- The product's existing read-only EIS/getDocsIP contour names the EIS SOAP token, SOAP enablement, TLS policy, and proxy-bypass controls as configuration categories. Secret values were not read. Local token and TLS-policy files are present outside the repositories; their contents and configured status were not inspected.

## 8. Ports / endpoints

The Arvectum OS reference contour is in-process and has no required network port. A `127.0.0.1` ephemeral bind passed. No public bind was attempted.

The product's existing optional local entry point uses configurable local port `8001` and binds `127.0.0.1`; that port is currently occupied by an existing localhost-only Python process and was not disturbed. It is product inventory only, not an Arvectum OS L2 requirement. All local endpoints remain **local-only** and are **not a Stable/public boundary**.

The EIS contour uses `zakupki.gov.ru` and `int.zakupki.gov.ru` outside the local host. Future authorized EIS work must preserve the product's explicit localhost/target-host proxy-bypass behavior as configured and fail closed if the verified TLS/network path is unavailable. L1 did not invoke EIS APIs or the live runner.

## 9. Disk and permissions

256 GiB is available on the intended workspace volume. With no asserted future document-byte total, this establishes no obvious storage blocker for a bounded seven-document evidence run. The checkout is readable and the local work-data probe passed without broad chmod/chown.

## 10. Rollback / removal

All L1-created local material is removable without system changes:

- `<local-root>/arvectum-os` — clean clone; recreate from canonical Git history;
- `<local-root>/runtime-data`, `<local-root>/evidence`, `<local-root>/tmp`, `<local-root>/local-config` — bounded local directories;
- any future venv/cache under `<local-root>` — remove as part of that local root.

The existing supplied empty Git directory and the existing `ai-corporation` checkout were not changed and are not L1 rollback targets.

## 11. Security / privacy observations

No secret values, private keys, cookies, certificates, proxy credentials, or token fragments were read into this evidence. No public ingress, system configuration change, privilege escalation, or external consequential action occurred. Configuration categories for later work are identified: EIS SOAP enablement/token, TLS-policy path and verification controls, EIS target-host proxy handling, and local runtime data/evidence paths.

## 12. Dogfooding friction

- The supplied `Arvectum-OS` directory was initialized but had no canonical history or remote, requiring a separate clean clone.
- The active PAC/proxy path reaches GitHub but times out for the two EIS hosts, which L3/L7 must diagnose through the existing fail-closed configuration rather than by changing system networking.

## 13. Blockers

None for L2. The EIS TLS/proxy timeout is a recorded prerequisite constraint for the later L3/L7 authorized contour, not a local reference-runtime blocker.

## 14. Exit-criteria assessment

- Host prerequisites inventoried: PASS.
- Repository locations and states inventoried: PASS.
- Runtime versions and compatibility inventoried: PASS.
- Local-only network/port assumptions inventoried: PASS.
- Disk and permissions sufficient: PASS.
- GitHub and EIS proxy constraints inventoried: PASS.
- Rollback/removal locations known: PASS.
- No final topology declared: PASS.

## 15. Disposition

`P6.05-L1: PASS`

`Next eligible action: P6.05-L2 — Reproducible Arvectum OS local checkout + reference runtime start.`
