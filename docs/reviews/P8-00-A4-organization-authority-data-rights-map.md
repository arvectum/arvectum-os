# P8.00-A4 — Organization / Identity / Authority / Data-Rights Map

Status: `Complete / PASS`
Version: `1.0.0`
Created: `2026-08-20`
Owner: `ООО «Арвектум»`
Task classification: `governance` with `platform` and `product_contract`
Roadmap work item: `P8.00-A4 — Organization / identity / authority / data-rights map`
Selected outcome: [`P8.00-A3`](P8-00-A3-bounded-external-outcome-selection.md)
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)

## 1. Result

**PASS — the selected EIS revalidation outcome has an explicit deny-by-default Organization, identity, authority and data-governance boundary.**

The validation uses one governing Organization only: `ООО «Арвектум»`. It does not claim validation of a second Organization or cross-Organization trust/isolation.

## 2. Boundary map

| Concern | Disposition |
|---|---|
| Governing Organization | `ООО «Арвектум»` |
| Technical tenant/isolation scope | existing owner-operated Arvectum OS Organization context; opaque runtime identifiers remain local and are not hard-coded into repository evidence |
| Product | Tender Operator |
| External system | ЕИС / `zakupki.gov.ru` |
| External authority mode | `External Reference` for EIS registry/document facts and source content |
| Product connector | product-owned read-only EIS retrieval path |
| Platform role | govern exact external observation/reference/version/freshness, provenance and reconstruction around product-owned retrieval |
| Cross-Organization access | denied / out of scope |
| External mutation | prohibited |
| Customer-facing service | out of scope |

## 3. Identity

Relevant semantic identities are kept distinct:

1. `ООО «Арвектум»` — governing Organization for the validation.
2. Owner/operator Principal — attributable human actor initiating or approving the bounded live validation.
3. Product/runtime service Principal — attributable local process/service acting within the explicit Organization scope where the implementation uses one.
4. ЕИС / `zakupki.gov.ru` — external authoritative system identity/reference.
5. Notice `0344100006426000005` — external object identifier in the EIS namespace; it is an external alias/reference, not automatically an Arvectum OS Subject Identity.
6. Any EIS user/token identifier — external authentication/credential context only; possession does not create Arvectum OS identity equivalence, authorization or Organizational Authority.

External identifiers must not be silently merged with Arvectum OS identities.

## 4. Authentication

Authentication evidence is contextual and does not create authority.

For the bounded live validation:

- EIS server identity/trust must be established through normal verified TLS;
- certificate verification and hostname verification must remain enabled;
- the previously exercised owner-operated truststore path may be used only without weakening verification;
- an individual-person token or equivalent existing EIS credential may be used only where the current product retrieval path requires it;
- reusable token/credential values, private material and raw authentication secrets remain outside canonical history, committed logs and evidence payloads;
- evidence may record only minimized non-secret facts needed to reconstruct that required authentication/trust conditions were satisfied.

A successful TLS handshake or token use does not establish legal rights, product authorization or Organizational Authority.

## 5. Authorization

Authorization for this validation is deliberately narrow:

Allowed technical operation:

- one bounded read-only retrieval/revalidation of the selected EIS notice/document source scope;
- local deterministic comparison with the preserved P6 evidence;
- governed admission/reference/provenance/reconstruction operations declared by the applicable Provisional platform boundary.

Denied by default:

- EIS/ETP write or mutation;
- procurement application submission;
- signature/EDS action;
- supplier/customer communication;
- broad crawling or unrelated EIS object access merely because credentials technically permit it;
- cross-Organization access;
- redistribution/publication of retrieved source documents through this Phase 8 validation.

Technical capability to perform a denied action does not authorize it.

## 6. Organizational Authority

Organizational Authority is separate from technical access.

- `ООО «Арвектум»` retains authority over whether this internal validation is performed and whether its results are accepted into Arvectum OS governance evidence.
- The owner remains residual decision authority because the Decision Authority Policy is still `Proposed 0.2.1` and no approved delegation supersedes owner authority.
- No Arvectum actor obtains authority over ЕИС state.
- No token, Product Contract, relationship, technical role or successful API call creates approval authority.
- No AI component may authorize the live retrieval scope, broaden the purpose, waive a failed trust/right gate or approve a later external commitment.

Phase 8 activation remains a separate A8 owner decision after A5–A7 pass.

## 7. Data Governance

### 7.1 Declared purpose

The only Phase 8 purpose is:

> validate governed reliance on a time-varying external authoritative source by comparing a fresh EIS observation with the preserved P6 observation and proving explicit freshness/version-drift handling.

Use outside that purpose is not authorized by this A4 map.

### 7.2 Data in scope

Minimum data/evidence may include:

- EIS notice number and external source namespace;
- source-listed document names/identifiers where safe and necessary;
- retrieval/observation timestamps;
- byte sizes and cryptographic integrity hashes;
- exact comparison disposition (`UNCHANGED`, `ADDED`, `REMOVED`, `CHANGED`);
- non-secret trust/retrieval outcome metadata;
- governed Arvectum OS references/versions/provenance needed for reconstruction.

### 7.3 Raw content and minimization

- Raw downloaded EIS documents/archive remain in the approved owner-local controlled runtime unless a later explicit governance decision changes that handling.
- Repository evidence should prefer names/identifiers, hashes, sizes, timestamps and minimized provenance over raw document content.
- Raw SOAP/XML payloads, archive URLs with sensitive query material, absolute local paths and reusable secrets must not be committed merely to prove the result.
- Product/debug telemetry remains non-canonical by default.

### 7.4 Classification / disclosure / export

The selected case uses publicly accessible procurement-source material in the already exercised product contour, but A4 does **not** convert technical/public accessibility into a complete legal or contractual rights determination.

Therefore:

- no broader redistribution right is asserted;
- no customer-facing disclosure right is asserted;
- no cross-Organization reuse right is asserted;
- export is limited to minimized internal governance/evidence records that do not disclose reusable secrets or unnecessary source payload;
- any later external disclosure or handover requires its own permitted-purpose and rights check.

### 7.5 Retention / deletion

- Retain only evidence necessary to reconstruct the bounded validation and preserve the historical P6/P8 comparison.
- Raw local source files should follow the existing owner-operated product/runtime retention rules and may be deleted when no longer required, provided the retained governed evidence does not overstate reconstructability.
- Deletion or minimization must not mutate already admitted historical Events/records; later state must represent omission/unavailability honestly.

## 8. Rights status

Known:

- a real read-only EIS retrieval path has already been exercised successfully in the owner-operated Tender Operator contour;
- the selected Phase 8 outcome requires no external mutation or redistribution;
- external source authority belongs to ЕИС for the declared registry/document scope.

Not established by current canonical evidence:

- a comprehensive legal/contractual permission basis for all possible EIS uses;
- redistribution rights;
- external customer service/support rights;
- cross-Organization reuse;
- mutation/submission/signature authority;
- a right to expose a stable public EIS integration service.

Unresolved rights fail closed. A4 is a governance boundary, not legal advice and not a rights-expansion decision.

## 9. Secrets and non-exportable material

Never place in canonical history or ordinary committed logs:

- EIS access tokens or equivalent reusable credentials;
- private keys/certificates or secret key material;
- password/recovery material;
- raw authentication headers;
- local secret-store identifiers when their disclosure would materially weaken security.

A portability/export package must represent required credential dependencies as omitted/reprovision-required rather than exporting reusable secrets.

## 10. Failure behavior

The validation must stop or remain explicitly incomplete when:

- Organization scope cannot be resolved unambiguously;
- authentication/trust evidence is insufficient;
- requested operation exceeds the read-only authorization envelope;
- Organizational Authority for the internal validation is absent;
- permitted purpose or rights for a requested broader use are unresolved;
- a secret would need to be copied into canonical history to proceed;
- external authority cannot be preserved without creating competing local truth.

No unresolved case may default to allow.

## 11. Cross-review

### Iteration 1 — identity/security

Separated EIS identifiers, credentials, Arvectum Principals and Organization scope; no identity implies permission.

### Iteration 2 — authority

Separated technical authorization from owner Organizational Authority and explicitly retained residual owner authority while the Decision Authority Policy remains Proposed.

### Iteration 3 — data rights/minimization

Removed any implication that public/technical accessibility proves broad legal rights; broader disclosure, redistribution and cross-Organization use remain deny-by-default.

**Result:** `PASS`; no material objection remains.

## 12. Handoff

A4 exit criteria are satisfied.

Next canonical action:

> **P8.00-A5 — Platform-responsibility necessity test.**
