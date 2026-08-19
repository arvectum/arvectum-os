# P7.10 — Implementation Readiness Review

Status: **Repository implementation PASS / canonical operational closure pending**  
Task: `P7.10 — Portability, host-loss and restore-on-clean-environment proof`  
Scope: `Persistent Internal / owner-operated`  
Implementation PR: `#83`  
Canonical implementation merge: `393cc5bff98cc87553b96d282f4bf618621fd87a`

## 1. Review conclusion

The repository-side P7.10 implementation is ready for the real selected-Mac portability exercise. It composes the existing P7.03 governed backup/restore primitive instead of introducing a competing persistence or authority path.

Two functional review/revise iterations were completed. The first found material package-boundary and release-identity weaknesses; those were remediated before merge. The second found no remaining material repository-design objection.

This review does **not** close P7.10. Actual selected-Mac host-loss/portability remains unproven until a verified handoff from the real P7.03 store is transferred off the selected Mac and restored on a genuinely clean secondary environment with a `PASS` receipt.

## 2. Canonical / architecture checks

Checked authority baseline:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0` as indexed canonically;
- no relevant Accepted ADR selects a permanent persistence/export/restore technology;
- P7.03 remains the owner of the bounded internal backup/archive format and restore primitive;
- P7.10 creates no lifecycle transition, Stable Product Contract, Active Platform Capability, Production/support commitment or public/stable recovery API.

No conflict with higher authority was identified.

## 3. Implemented evidence boundary

The P7.10 handoff contains only:

- a verified P7.03 archive;
- its P7.03 SHA-256 sidecar;
- a P7.10 portability manifest;
- the manifest SHA-256 sidecar.

Verification fails closed on missing or extra package members, symlinks/directories inside the handoff, checksum mismatch, Organization-scope mismatch, archive-integrity failure, release-identity mismatch, reusable-secret inclusion, authority-boundary violation or a dirty restore target.

The P7.10 envelope release SHA is explicitly bound to the release identity embedded in the P7.03 archive manifest. This prevents an independently edited P7.10 envelope from making a false exact-release claim while retaining a valid underlying P7.03 archive.

## 4. Historical continuity proof

The mechanism requires at least one governed historical item. A successful empty-store archive round-trip is therefore insufficient for P7.10.

The source records a host-independent digest of governed state and a deterministic selected historical record carrying, as applicable:

- semantic/schema identity;
- classification and retention reference;
- Subject and exact Version identity;
- authority mode and scope;
- governed admission reference;
- source release;
- provenance references;
- payload SHA-256.

The clean target must reconstruct matching semantic evidence after P7.03 restore.

## 5. Security / authority review

The implementation preserves the following boundaries:

- reusable secrets are not exported or restored;
- runtime `run/`, logs and cache are not restored as governed state;
- telemetry remains non-canonical;
- technical restore grants no Organizational Authority or consequential approval;
- historical reconstruction performs no external-effect replay;
- machine-local service-manager, network/proxy/TLS and credential configuration remains target-environment reprovisioning, not portable semantic state.

Checksum evidence is treated as integrity evidence only. It is not represented as cryptographic authenticity, signer identity or Organizational Authority.

## 6. `/var` → `/private/var` portability finding

P7.09 preserved a selected-Mac full-suite discrepancy caused by lexical `/var/...` versus resolved `/private/var/...` paths.

P7.10 resolves the classification without hiding the observation:

- the lexical path is retained as operator/evidence context;
- physical security/location comparisons use filesystem identity (`samefile` where available) or resolved physical paths;
- when `/var` and `/private/var` resolve to the same filesystem object, the difference is a host path-presentation alias, not semantic-state divergence;
- a future lexical alias that resolves to a different physical object remains a material environment/configuration difference and must fail closed where the boundary requires same-location identity.

The P7.10 macOS CI job explicitly proves the real `/var` alias behavior; unit coverage also reproduces it with a symlink fixture.

## 7. Repository evidence

Final PR head: `d79defc54a3276e616bf72037b0dea14efd6e9bc`.

Repository checks before merge:

- `Reference Python CI #164`, run `32274126879` — `success`;
- full suite — `1191 tests`, `OK`;
- final `P7.10 Portability Proof #4`, run `32274126875` — `success`;
- macOS source handoff job — `success`;
- independent Linux clean-secondary restore job — `success`.

The automated proof transfers only the off-host handoff artifact between independent jobs. The Linux restore job proves the source runtime and clean target are absent before restoration, reconstructs governed history and emits a bounded receipt.

This automated proof establishes the mechanism and cross-OS clean-runner behavior. It is not substituted for the real selected-Mac operational proof.

## 8. Functional review iterations

### Iteration 1 — revise

Material objections found and fixed:

1. The handoff verifier originally did not require an exact package-member set. Remediation rejects undeclared files and non-regular members.
2. The P7.10 envelope release SHA was not originally bound to the P7.03 archive manifest. Remediation verifies exact equality against the archive's own release identity.
3. Historical evidence was expanded to preserve classification, retention and authority-scope context in addition to identity/provenance/payload digest.
4. The dedicated workflow was extended to support proof on canonical `main`, not only pull-request validation.

### Iteration 2 — pass

Cross-review of authority separation, security/exclusions, persistence ownership, path portability, historical reconstruction and commercial/lifecycle non-claims found no remaining material repository-design objection.

Use of the P7.03 internal archive-reader inside the same internal reference implementation is bounded and does not establish a public/stable interface. P7.03 remains the semantic owner of the archive format.

## 9. Remaining P7.10 operational proof

Before P7.10 can become `Complete / PASS`, all of the following remain required:

1. use the real selected Mac's P7.03 governed store as source;
2. create and verify the P7.10 handoff without reusable secrets;
3. physically transfer the package beyond the selected-Mac runtime/host-loss boundary through an owner-controlled medium;
4. on a genuinely clean secondary environment at the exact canonical release, restore into an absent target;
5. obtain a `PASS` clean-restore receipt with matching governed-state and selected-history evidence;
6. minimize any host/path information before canonical publication while retaining sufficient evidence;
7. perform final P7.10 closure review and synchronize the canonical roadmap;
8. only then proceed to `R23 — Recovery / Portability Review`.

Until this evidence exists, `M7` criterion 10 is not claimed satisfied and R23 remains downstream.
