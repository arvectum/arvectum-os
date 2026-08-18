# P7.06-UI1 Selected-Mac Live-Browser Proof — Attempt 1

Status: `BLOCKED — operational proof passed; no real retained governed item available`
Date: `2026-08-18`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `governance`
Operating scope: `Persistent Internal / owner-operated`

## 1. Purpose

This review records the first selected-Mac closure attempt for `P7.06-UI1 — Live read-only governed workspace` after the repository implementation merged through PR `#51`.

The attempt successfully proved the exact-release deployment, private browser surface, least-privilege read authorization, fail-closed negative paths and read-only behavior on the selected Mac. It does **not** close UI1 because the persistent P7.03 store contained no real retained `canonical-governed-state` item to inspect.

The blocker is therefore absence of qualifying live governed state, not failure of the UI1 adapter itself.

## 2. Authority and boundary

The disposition is checked against:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- `P7.03` durable governed-state boundary;
- `P7.04` least-privilege persistent access boundary;
- `P7.05` persistent runtime health/visibility boundary;
- `P7.06` governed deployment/update boundary;
- the active live-workspace substream and UI1 exit evidence.

P7.03 may persist canonical governed bytes only after an applicable Governed Execution/admission path has already authorized and produced them. This attempt therefore does not manufacture a record merely to satisfy the UI exit criterion, and a `governed-test-fixture` is not accepted as a substitute for real retained governed state.

## 3. Exact release deployment

Canonical checkout at execution:

- repository: `arvectum/arvectum-os`;
- branch: `main`;
- canonical/local exact SHA: `3a2b561a6935a84749552f016db8d1bd69eabf9a`;
- tracked working tree: clean.

P7.06 governed update evidence:

- previous active release: `4df99c4c66a1b7b93a4b05d7768018b03aa4041b`;
- target/final active release: `3a2b561a6935a84749552f016db8d1bd69eabf9a`;
- preflight: `PASS`;
- update: `PASS`;
- deployment transaction: `0a858c2b44709516f49829cde7c8a45c4df6e9316303066ce879f341cbda25c5`;
- verified pre-update backup: `PASS`;
- backup SHA-256: `1a1ccb84d4922f08fc860d3ad2e995f4e2283e3c138223a1daf81cb4ee88f3c7`;
- migration disposition: `none`;
- runtime exact-release health: `PASS`;
- observer exact-release pin: `PASS`.

No schema-changing migration, product/external effect or historical effect replay was invoked by this deployment.

## 4. Owner context and access

The attempt reused the already-established P6.05-L4 Organization context and attributable human owner-operated Principal. No new Organization or human Principal was created.

P7.04 evidence:

- persistent access store verification: `PASS`;
- credential secret exposure: `NO`;
- exact grant semantics: `workspace.inspect / workspace:p7-06-ui1 / local`;
- revoked-grant test: `PASS`;
- access restored by a new exact grant without restarting UI1: `PASS`;
- Organizational Authority satisfied by access: `NO`;
- consequential approval satisfied by access: `NO`.

Opaque Organization/Principal values, credential identifiers and grant identifiers remain owner-local and are intentionally omitted from canonical repository evidence.

## 5. Real browser / HTTP proof

UI1 was executed from the exact active release rather than the mutable Git working tree.

Browser proof:

- browser: Safari;
- bind address: IPv4 loopback only;
- port: `8766` because `8765` was already occupied by an unrelated owner-local AgentDock process;
- real browser opened: `YES`;
- owner visual confirmation: `YES`;
- runtime release/health context visible: `PASS`;
- `Discover / Records / Executions / Evidence / Documents / Knowledge`: reachable;
- missing metadata fabricated: `NO`;
- governed payload bytes rendered: `NO`;
- governed-test fixture used as proof: `NO`.

HTTP evidence:

- `GET`: `200`;
- `HEAD`: `200`;
- `POST`: `405`;
- `PUT`: `405`;
- `PATCH`: `405`;
- `DELETE`: `405`;
- no-store/CSP/referrer/nosniff/frame-denial headers: `PASS`.

Negative-path evidence:

- wrong/unresolved Organization fails closed: `PASS`;
- protected counts/content leaked on wrong Organization: `NO`;
- revoked exact grant fails closed without workspace restart: `PASS`;
- subsequent exact re-grant restores access without workspace restart: `PASS`.

## 6. Read-only / mutation evidence

Before and after authorized browsing, the governed P7.03 item set was empty and unchanged.

Result:

- canonical governed-state mutation by browsing: `NO`;
- product external effect: `NO`;
- historical effect replay: `NO`;
- final P7.06 status: `PASS`;
- final runtime health: `PASS`;
- final observer status: `PASS`;
- final P7.04 store verification: `PASS`;
- canonical repository working tree after proof: clean;
- UI1 foreground process after proof: stopped.

Owner-local bounded evidence is retained outside Git. Its SHA-256 is:

`ee153d84917839fb7566794f4227c19ae7eb4efd0de25596a3eaf3dcbb8f5364`

The canonical repository does not contain the credential secret, owner-local evidence payload or governed payload bytes.

## 7. Blocking condition

The live authorized workspace reported:

- Records: `0`;
- Executions: `0`;
- Documents: `0`;
- Knowledge: `0`;
- qualifying real non-fixture governed item: `NONE`.

Therefore Subject/Exact-Version/provenance inspection over a **real retained canonical governed item** could not be demonstrated.

Creating an arbitrary P7.03 `canonical-governed-state` entry only to make UI1 pass would violate the persistence/admission boundary: P7.03 does not itself authorize canonical truth or consequential canonical mutation.

## 8. Canonical unblock disposition

The next bounded unblock is to establish at least one real retained governed item through an already-applicable Governed Execution/admission path and only then persist the admitted bytes/metadata through P7.03.

Existing Phase 6 evidence provides a strong candidate input: P6.05-L7 retained real exact EIS attachment evidence for notice `0344100006426000005`, and P6.05-L8 separately proved CAP-001 governed admission, Event/provenance and reconstruction without repeating EIS retrieval or invoking external actions.

However the historical P6.05-L8 reference harness uses its own bounded `p6-05-org-a` execution context. It must **not** be copied into the current persistent store as if it were the current owner context. Any new persistent admission must preserve the actual existing P6.05-L4 Organization/human-operator continuity, applicable Product Contract/authority semantics and the normal RFC-0005 gates.

No EIS refetch, raw-payload platformization, external effect, hidden authority substitution or fixture promotion is authorized by this review.

## 9. Final disposition

- repository UI1 implementation: `PASS`;
- selected-Mac exact-release/browser/auth/read-only proof: `PASS` for exercised paths;
- real retained governed-item inspection: `BLOCKED — no qualifying item exists in P7.03`;
- `P7.06-UI1`: remains `Current`;
- `P7.06-UI2`: remains `Pending / not started`;
- lifecycle promotion: `none`;
- Product Contract lifecycle change: `none`;
- public/stable UI/API boundary: `none`.

`P7.06-UI1 SELECTED-MAC ATTEMPT 1 = BLOCKED` solely on absence of real retained canonical governed state.