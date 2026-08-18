# P7.06-UI1 — Live Read-Only Governed Workspace

Status: `Repository implementation PASS; selected-Mac closure pending`
Date: `2026-08-18`
Task classification: `platform` (with operational-governance constraints)
Operating scope: `Persistent Internal / owner-operated`

## 1. Purpose

P7.06-UI1 connects the completed M4 workspace presentation semantics to the selected persistent Arvectum OS runtime through a bounded private read-only adapter.

It does not create a public/stable UI or API, a frontend-framework commitment, an Organizational Authority source, an approval path, a Product Contract, an `Active` Platform Capability, customer Production support, a browser support matrix or an SLA/support commitment.

## 2. Canonical authority checked

The implementation was checked against:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- canonical roadmap and `P7-06-LIVE-OPERATOR-WORKSPACE-SUBSTREAM.md`;
- existing M4 workspace shell semantics;
- P7.03 durable governed-state/checkpoint storage;
- P7.04 persistent identity/access enforcement;
- P7.05 operational health classification;
- P7.06 exact-release governed deployment/runtime pinning.

No Accepted ADR currently selects a frontend framework, public service/API, browser matrix or permanent UI transport. This private reversible adapter does not require a new ADR.

## 3. Repository implementation

Canonical implementation file:

- `reference/python/p7_06_ui1_live_workspace.py`

Executable evidence:

- `reference/python/tests/test_p7_06_ui1_live_workspace.py`

The adapter:

1. accepts an explicit Organization identity and attributable human Principal;
2. requires the exact P7.04 grant:
   - operation: `workspace.inspect`;
   - resource: `workspace:p7-06-ui1`;
   - access path: `local`;
3. authorizes before reading governed-state contents or counts;
4. requires execution from the exact currently activated P7.06 release and requires P7.05 health to identify that same release as healthy;
5. reads verified P7.03 canonical governed-item manifests and recovery checkpoints;
6. excludes `governed-test-fixture` state from live surfaces;
7. exposes the M4 destinations `Discover`, `Records`, `Executions`, `Evidence`, `Documents`, `Knowledge`;
8. makes Subject and Exact Version visibly distinct;
9. shows authority/source/lifecycle/validation metadata only when retained, and labels missing metadata as missing instead of inferring it;
10. keeps checkpoint evidence explicitly non-authoritative;
11. never renders governed payload bytes;
12. binds only to explicit IPv4 loopback;
13. supports only `GET` and `HEAD`; `POST`, `PUT`, `PATCH`, and `DELETE` are rejected;
14. re-authorizes every request so credential/grant revocation takes effect without restarting the workspace;
15. uses generic blocked responses that do not expose protected content, identifiers or counts;
16. fails closed when the governed store/checkpoint store is unavailable, unsafe or contains unexpected entries.

## 4. Read-only / authority boundary

The workspace is a presentation adapter over already-authorized retained state.

It does not:

- create or modify Canonical Records;
- create or modify governed checkpoints;
- invoke Governed Execution mutation paths;
- grant/revoke access;
- issue/rotate credentials;
- emit operational telemetry as part of reads;
- call external/product effects;
- convert telemetry, checkpoints, search/grouping or UI projections into authority;
- satisfy Organizational Authority or consequential approval.

The UI grouping of retained `semantic_type` values into M4 destinations is explicitly non-authoritative presentation only.

## 5. Repository evidence

PR `#51` contains the implementation and regression tests.

Repository review required two functional iterations:

- iteration 1 found that a missing P7.03 store could be displayed as an empty collection and that unexpected checkpoint-store entries could be silently skipped;
- iteration 2 changed both cases to fail closed and added regression tests.

GitHub `Reference Python CI` run `32132213609` on head `83fb21f19ae99552c8a1a665a94a32e9f008da4c` completed with `success` after the remediation.

Repository-side result: `PASS`.

## 6. Selected-Mac closure still required

Repository evidence alone is insufficient for `P7.06-UI1 = Complete / PASS`.

The canonical substream requires owner-operated live evidence from the selected Mac:

1. merge the repository implementation to canonical `main`;
2. use the already-proven P7.06 governed deployment/update path to activate the exact merged release on the selected persistent runtime;
3. preserve/reuse the existing P6.05-L4 Organization and attributable human operator identity;
4. establish only the exact P7.04 local `workspace.inspect` / `workspace:p7-06-ui1` grant for that existing human operator;
5. run `p7_06_ui1_live_workspace.py` from the exact activated release, not from a working tree;
6. open the loopback workspace in a real browser on the selected Mac;
7. verify the visible Organization, Actor, exact release, healthy runtime state and all M4 information-architecture destinations;
8. inspect at least one real retained canonical governed item/provenance record, not a generated fixture;
9. verify Subject and Exact Version are presented distinctly and that unavailable metadata is not fabricated;
10. verify an incorrect/unresolved Organization or revoked grant fails closed without protected counts/content;
11. verify read-only browsing changes neither governed-state contents nor canonical/external state;
12. record bounded non-secret owner-local evidence and its digest for canonical review.

Until those steps pass, `P7.06-UI1` remains `Current`; `P7.06-UI2` must not be advanced canonically.

## 7. Governance disposition

- Constitution conflict: `none found`.
- Accepted RFC conflict: `none found`.
- New RFC required: `no`.
- New ADR required: `no` for the current private/reversible scope.
- Lifecycle promotion: `none`.
- Product Contract change: `none`.
- Public/stable boundary created: `no`.
