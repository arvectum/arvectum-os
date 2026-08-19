# P7.10 — Portability, host-loss and restore-on-clean-environment proof

Status: **Implementation + automated cross-host mechanism proof**  
Canonical roadmap item: `P7.10`  
Scope: `Persistent Internal / owner-operated`  
Lifecycle/conformance effect: **none**

## 1. Purpose

P7.10 proves that governed organizational state can leave the selected host as a verified recovery package and be reconstructed on a clean secondary environment without turning backup/restore into a second authority path.

This work composes the P7.03 durable-state backup/restore primitive. It does **not** define a new canonical-state format, authorize replay of external effects, copy reusable credentials, promote a Product Contract or Platform Capability, or create a Production/support commitment.

## 2. Authority basis and boundaries

The proof is constrained by the Ratified Constitution and Accepted RFC-0001, RFC-0003, RFC-0005, RFC-0006 and RFC-0008:

- semantic organizational identity, provenance and governed state must survive host/technology changes;
- export/portability must preserve organization scope, identities/versions, authority semantics, provenance, classification/retention metadata and integrity evidence as applicable;
- reusable secrets/credentials are not made portable merely for proof convenience;
- telemetry/runtime cache/logs remain non-canonical and are excluded;
- technical restore creates no Organizational Authority or consequential approval;
- historical reconstruction never re-performs an external effect without a new governed authorization.

P7.03 remains the backup/archive authority for this internal implementation. P7.10 adds an **off-host handoff envelope and proof receipt**, not a competing backup mechanism.

## 3. Proof model

The implementation has two evidence layers.

### 3.1 Automated independent-runner mechanism proof

`.github/workflows/p7-10-portability-proof.yml` performs a two-job transfer:

1. `macos-latest` constructs a governed P7.03 fixture containing at least one canonical governed record and checkpoint.
2. P7.03 creates and verifies its owner-local archive/checksum.
3. P7.10 copies only that verified archive/checksum into an off-host handoff directory and records semantic/path/host evidence.
4. GitHub artifact transfer crosses the job boundary; the source runtime is not transferred.
5. A separate `ubuntu-latest` runner downloads only the handoff package, proves the source runtime and restore target are absent, and restores into the clean target.
6. The target verifies P7.03 integrity, a host-independent governed-state digest, selected historical identity/version/provenance/payload digest, exclusions, and no-effect-replay/no-authority-escalation assertions.
7. A minimized clean-restore receipt is emitted as CI evidence.

This proves the **mechanism** is not coupled to one OS process tree, absolute runtime root, or source workspace.

### 3.2 Selected-Mac operational host-loss proof

Automated CI does not impersonate the actual selected Mac mini. Canonical P7.10 closure therefore also requires one real off-host handoff from the selected Mac's P7.03 store and restoration on an actually clean secondary environment.

The selected-Mac persistent runtime root is the same root already used and verified by the P7.09 selected-Mac closure:

```bash
export ARVECTUM_P7_02_ROOT="${HOME}/Library/Application Support/ArvectumOS/persistent-internal"
```

The source command is intentionally separate from the clean-host command:

```bash
PYTHONPATH=reference/python python reference/python/p7_10_portability_proof.py prepare \
  --source-root "${ARVECTUM_P7_02_ROOT}" \
  --off-host-dir /PATH/OUTSIDE/THE/PRIMARY/HOST/RUNTIME/p7-10-handoff \
  --release-sha <exact-canonical-release-sha> \
  --host-marker <selected-mac-host-marker>
```

Do not substitute `/var/lib/arvectum-os` for the selected-Mac runtime root. The `/var` versus `/private/var` case discussed in §5 is portability/path-alias evidence from the macOS environment and is **not** the selected-Mac persistent runtime location.

Transfer the resulting directory through the chosen owner-controlled off-host medium. Do **not** copy the live runtime tree or secrets as a shortcut.

On a clean secondary checkout at the exact release SHA, create or verify an **owner-only immediate parent** for the restore target. P7.03 stages and atomically publishes the restored store inside `target_root.parent`; an existing parent with group/other permissions therefore fails closed. A normal macOS home directory may be `0750`, so do not place the restore target directly under `$HOME` merely for convenience.

Example:

```bash
RESTORE_PARENT="${HOME}/p7-10-proof"

if [ ! -e "${RESTORE_PARENT}" ]; then
  mkdir -m 700 "${RESTORE_PARENT}"
fi

test -d "${RESTORE_PARENT}"
test ! -L "${RESTORE_PARENT}"
test "$(stat -f '%Lp' "${RESTORE_PARENT}" 2>/dev/null || stat -c '%a' "${RESTORE_PARENT}")" = "700"

TARGET="${RESTORE_PARENT}/clean-arvectum-os-runtime"
RECEIPT="${RESTORE_PARENT}/p7-10-clean-restore-receipt.json"

test ! -e "${TARGET}"
test ! -e "${RECEIPT}"

PYTHONPATH=reference/python python reference/python/p7_10_portability_proof.py restore \
  --package-dir /PATH/TO/TRANSFERRED/p7-10-handoff \
  --target-root "${TARGET}" \
  --release-sha <exact-canonical-release-sha> \
  --host-marker <clean-secondary-host-marker> \
  --receipt "${RECEIPT}"
```

Do not weaken the P7.03 owner-only parent rule by changing a system/user home-directory permission policy merely to make the proof pass. Do not silently `chmod` an existing restore parent to force a pass. Use a bounded owner-only restore parent under the operator-controlled environment and fail closed if an existing parent does not already satisfy the required boundary.

The receipt is evidence, not approval. It should be minimized before canonical publication if hostnames or local absolute paths disclose unnecessary operator information.

## 4. Handoff contents

The off-host handoff contains exactly:

- the verified P7.03 `*.tar.gz` archive;
- its P7.03 `*.sha256` sidecar;
- `p7-10-portability-manifest.json`;
- `p7-10-portability-manifest.json.sha256`.

The P7.10 manifest records:

- Organization scope;
- exact tool/release SHA;
- source host marker and environment facts used only as portability evidence;
- source lexical and physical path identities;
- P7.03 archive digest/integrity;
- host-independent governed-state digest;
- one deterministically selected historical record with subject/version/authority/source-release/provenance/payload digest;
- explicit non-exportables and no-replay/no-authority claims;
- host-specific configuration that must be re-established separately.

## 5. `/var` vs `/private/var` discrepancy disposition

P7.09 observed selected-Mac full-suite failures caused by lexical `/var/...` versus resolved `/private/var/...` path presentation.

P7.10 does **not** suppress or stringify this difference away. It records both forms and applies two distinct rules:

1. **Evidence/UI/operator path:** preserve the lexical path that was supplied.
2. **Filesystem security/location comparison:** compare physical filesystem identity (`os.path.samefile` when possible, otherwise resolved physical paths).

The dedicated macOS CI probe requires `/var` and `/private/var` to resolve to the same filesystem location while retaining lexical inequality. The unit suite also reproduces the condition with an explicit symlink fixture.

Disposition: when the two names identify the same filesystem object, the discrepancy is a **host path-presentation alias**, not a semantic-state difference and not a reason to weaken P7.03's physical path boundary checks. A future case in which lexical aliases resolve to different filesystem objects must fail closed and be treated as a material environment/configuration difference.

## 6. Clean-environment invariants

A restore passes only when all of the following hold:

- the target root is absent before restoration;
- the immediate restore parent is an existing owner-only, non-symlink directory on POSIX hosts, or is created by the bounded operator procedure with equivalent owner-only semantics;
- the source and target host markers are distinct;
- the exact release SHA matches the handoff;
- manifest and archive checksums verify;
- P7.03 restore integrity is `PASS`;
- the restored governed-state digest equals the source digest;
- the selected historical record reconstructs with identical identity/version/authority/provenance/payload evidence;
- `secrets/`, `run/`, `logs/`, and `cache/` are not recreated by restore;
- reusable secrets are not transferred or restored;
- external-effect replay is false;
- restore grants no Organizational Authority.

Any violated invariant fails closed.

## 7. Host-specific configuration intentionally outside the package

The following are adapters/configuration, not portable semantic state:

- absolute runtime root;
- launchd/systemd/other service-manager persistence;
- machine-local credentials and secret material;
- network/proxy/TLS configuration;
- OS-specific filesystem aliases and ownership/permission plumbing.

These must be reprovisioned or re-established for the target environment. Their absence from the package is intentional and must not be repaired by copying machine-local secrets.

## 8. Evidence and closure rule

Automated proof plus unit tests establish cross-OS clean-runner portability of the implementation mechanism. They are necessary but not sufficient to claim loss of the **actual selected Mac** has been operationally recovered.

P7.10 may be marked `Complete / PASS` only after:

1. the automated proof is green at the canonical implementation SHA;
2. a selected-Mac off-host handoff is created from the real P7.03 governed store without reusable secrets;
3. that handoff is restored on a clean secondary environment with a `PASS` receipt;
4. the minimized evidence and `/var` disposition are reviewed for R23 readiness;
5. roadmap state is synchronized.

Until those conditions are met, the honest status is **implementation ready; selected-Mac operational proof pending**.
