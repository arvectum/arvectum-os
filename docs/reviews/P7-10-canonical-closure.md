# P7.10 — Canonical Closure

Status: **Complete / PASS**  
Date: `2026-08-19`  
Task: `P7.10 — Portability, host-loss and restore-on-clean-environment proof`  
Scope: `Persistent Internal / owner-operated`  
Task classification: `platform`

## 1. Closure conclusion

P7.10 is `Complete / PASS` for the declared `Persistent Internal / owner-operated` scope.

The real selected-Mac P7.03 governed store was packaged into the bounded P7.10 four-member handoff, transferred beyond the selected-host loss boundary through an owner-controlled encrypted off-host medium, re-verified byte-for-byte on a separate clean secondary Mac, and restored into a fresh absent target using the exact release identity embedded in the handoff.

The clean-secondary restore returned `PASS`; P7.03 integrity remained `PASS`; the host-independent governed-state digest matched the source handoff; selected historical reconstruction passed; reusable secrets were not restored; no external effect was replayed; technical restore granted no Organizational Authority; and the explicitly excluded `secrets/`, `run/`, `logs/`, and `cache/` paths were absent.

This closes the operational gap left by the repository implementation/readiness proof. M7 criterion 10 is therefore satisfied for the declared scope. `R23 — Recovery / Portability Review` is the next canonical gate before P7.11 lifecycle/readiness disposition.

## 2. Authority and architecture basis

Closure was checked against:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- especially RFC-0001 portability/security invariants and RFC-0003 identity/security/privacy/tenant-sovereignty/portability separation;
- RFC-0005 Governed Execution authority boundaries;
- RFC-0006 event/provenance/reconstruction boundaries;
- RFC-0008 artifact/transient-output boundaries;
- P7.03 as the bounded internal backup/archive semantic owner;
- the canonical Phase 7 sequencing that places R23 after P7.10.

No relevant Accepted ADR selects a permanent persistence, export, backup, restore or host technology. No higher-authority conflict was identified.

Technical recovery remains distinct from Authorization, Organizational Authority, consequential approval and Data Governance. This closure does not convert recovery evidence into an authority source.

## 3. Repository and implementation evidence

Repository implementation and automated mechanism proof were previously closed as ready through:

- implementation PR `#83`, canonical merge `393cc5bff98cc87553b96d282f4bf618621fd87a`;
- final implementation head `d79defc54a3276e616bf72037b0dea14efd6e9bc`;
- `Reference Python CI #164`, run `32274126879` — `success`, `1191 tests / OK`;
- `P7.10 Portability Proof #4`, run `32274126875` — `success`;
- independent macOS source-handoff and Linux clean-secondary jobs — `success`.

The selected-Mac operational exercise subsequently exposed and preserved two operator-environment/instruction defects rather than weakening the implementation:

1. an initial source-path instruction incorrectly used `/var/lib/arvectum-os` instead of the already-established selected-Mac persistent root; the operator stopped fail-closed and the documentation was corrected;
2. operational Attempt 2 restored directly beneath a secondary macOS home directory with mode `0750`; P7.03 correctly rejected the immediate restore parent before target publication. The failure is preserved in [`P7.10 — Selected-Mac Operational Attempt 2`](P7-10-selected-mac-attempt-2-clean-parent-failure.md).

PR `#86`, merge `16621a1abc814a92e8fed0d0a3451946be6f8303`, preserved the P7.03 owner-only immediate-parent security boundary, corrected the P7.10 operational instructions and added regression coverage. Final Reference Python CI passed `1192 tests / OK`, including the explicit `0750` fail-closed → dedicated `0700` restore-parent success regression; the P7.10 automated portability workflow also passed.

PR `#87`, merge `de59771281ce1b4c58d943bd003560384e332270`, corrected the Attempt 3 exact-release procedure: the already transferred handoff must be restored at its own embedded canonical release rather than relabelled with a later documentation/test-only merge. The runtime implementation files `p7_10_portability_proof.py` and `p7_03_durable_state.py` were unchanged by those corrections.

## 4. Attempt 3 owner-local evidence

Attempt 3 reused the same unchanged handoff produced and transferred during Attempt 2. Canonical history intentionally retains only minimized operational evidence; raw local paths, local hostnames and the full receipt remain owner-local.

Exact handoff/tool release:

- `fbab170ab337c1631b40d0d36ea58a02f6512f6e`.

Handoff verification:

- verify before Attempt 3: `PASS`;
- exact regular-file count: `4`;
- archive SHA-256: `074f2a4e84e222bd26d6ed21a829aa0dcc1c91834479345cfa652405b721bfbd`;
- P7.10 manifest SHA-256: `fe0d2c7d9460f9da4356a3a3f7419b825b8aef3a8d18123ab35fb0281db3ada9`;
- both digests matched the previously transferred Attempt 2 evidence byte-for-byte.

Clean-secondary environment:

- separate MacBook Air host;
- macOS `26.6.2`;
- `arm64`;
- Python `3.9.6`;
- source and target host markers were distinct;
- dedicated immediate restore parent was a non-symlink owner-only directory with mode `0700`;
- the restore target and receipt were absent before Attempt 3;
- the ordinary macOS home-directory mode remained unchanged; no system/home permission policy was weakened to obtain a pass.

Restore result:

- result: `PASS`;
- P7.03 integrity: `PASS`;
- governed-state SHA-256: `da558333e0d98beac96298703326ca9d660db9098a3b0f2aa94b18c14d5a07a1`;
- selected historical reconstruction: `PASS`;
- restored governed items: `2`;
- restored checkpoints: `2`;
- reusable secrets restored: `NO`;
- external-effect replay performed: `NO`;
- Organizational Authority granted by restore: `NO`;
- forbidden restore paths absent: `YES`.

Owner-local clean-restore receipt:

- basename: `p7-10-clean-restore-receipt-attempt-3.json`;
- SHA-256: `ab7bf132d3d3a1304e3582c25fbd80a783d36c7bee9e5e6439ed4c54780aa341`.

The receipt is operational evidence, not an approval or authority artifact.

## 5. Exact-release and state-continuity disposition

The handoff release is `fbab170ab337c1631b40d0d36ea58a02f6512f6e`. Attempt 3 deliberately used an exact detached checkout of that release because P7.10 binds the envelope release to the P7.03 archive's embedded release identity.

The retained store also preserved its historical persistent-runtime release context. This does not create a requirement that the clean target impersonate the old host or reactivate external effects; it demonstrates that governed state and its historical release/provenance context survive host loss independently of machine-local service configuration.

The restored governed-state digest equals the digest already observed during the selected-Mac P7.07 continuity proof. P7.10 therefore demonstrates semantic continuity of the actual retained governed state, not merely a synthetic or empty backup round-trip.

## 6. `/var` → `/private/var` portability disposition

P7.09 preserved an environment-specific lexical `/var/...` versus physical `/private/var/...` full-suite discrepancy. P7.10 did not normalize that observation away.

The final disposition remains:

- lexical path is operator/evidence presentation context;
- security/location checks use physical filesystem identity where path equivalence matters;
- `/var` and `/private/var` are a host path-presentation alias only when they resolve to the same filesystem object;
- a lexical alias resolving to a different physical object remains a material environment/configuration difference and must fail closed where same-location identity is required;
- the actual selected-Mac persistent P7.03 source was the established owner-local runtime root, not `/var/lib/arvectum-os`.

Automated macOS CI proves the real `/var` alias behavior, unit coverage reproduces it with an explicit symlink fixture, and the real clean-secondary restore passed without relying on `/var` as the selected-Mac state root.

The P7.09 discrepancy is therefore classified as a host path-presentation/environment issue with an explicit physical-identity rule, not semantic-state divergence and not a reason to weaken P7.03 security boundaries.

## 7. Portability limits and non-claims

P7.10 proves bounded portability of governed organizational state beyond the selected Mac mini for the declared internal owner-operated scope. It does not prove or promise universal host portability.

The following remain host/environment-specific and must be reprovisioned separately where applicable:

- absolute runtime roots;
- launchd/systemd/other service-manager configuration;
- machine-local credentials and reusable secrets;
- network/proxy/TLS configuration;
- OS-specific filesystem/ownership plumbing.

P7.10 does **not** establish:

- external/customer `Production` readiness;
- an `Active` Platform Capability;
- a `Stable` Product Contract;
- a public/stable backup, restore, export or migration API/format;
- a permanent storage or deployment technology decision;
- SLA/SLO/RPO/RTO/support commitments;
- full-platform or cross-environment conformance;
- authority to replay historical external effects;
- authority or approval merely because data was technically restored.

## 8. Functional closure review

### Iteration 1 — revise/minimize

The submitted Attempt 3 result satisfied the technical exit criteria, but canonical publication was reviewed for evidence minimization and exact-release semantics. The raw absolute paths and local hostnames were not required for durable canonical understanding and are therefore not copied into this closure; owner-local raw evidence is retained by receipt basename and SHA-256. The handoff remains attributed to its exact embedded release rather than the later documentation/test-only correction merges.

No security rule was weakened and no failed attempt was rewritten into a pass.

### Iteration 2 — PASS

Cross-review of portability, exact-release identity, P7.03 ownership, semantic-state continuity, historical reconstruction, secrets/exclusions, authority separation, effect replay, `/var` disposition, lifecycle/commercial non-claims and Phase 7 sequencing found no remaining material objection.

Result: `PASS`.

This functional review is evidence for task closure only. It is not a lifecycle promotion, formal Production approval, Product Contract stabilization or Platform Capability activation.

## 9. Closure state and next action

`P7.10 = Complete / PASS` for the declared `Persistent Internal / owner-operated` scope.

`M7 criterion 10 = satisfied`.

Criteria 11–13 remain downstream.

The next canonical action is:

> **R23 — Recovery / Portability Review.**

R23 must review the accumulated P7.03/P7.06/P7.09/P7.10 recovery and portability evidence before P7.11 performs lifecycle, conformance and stable-boundary disposition.
