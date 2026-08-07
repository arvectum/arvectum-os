# RFC State Transition Procedure

Status: `Approved`
Version: `1.0.0`
Effective: `2026-08-07`
Owner: `ООО «Арвектум»`
Category: `governance`
Approval evidence: `DECISION-2026-08-07-RFC-STATE-TRANSITION-CLOSURE`

## Purpose

Prevent stale RFC status from carrying across project chats and ensure that owner approval, canonical publication and roadmap state advance together.

## Mandatory transition closure

When the owner explicitly approves RFC-N, the same working cycle MUST complete the following sequence before substantive work starts on RFC-(N+1):

```text
Owner approval
    ↓
Canonical approval decision
    ↓
RFC-N published as Accepted
    ↓
RFC Index synchronized
    ↓
Canonical roadmap synchronized
    ↓
Read-after-write refresh from default branch
    ↓
Cross-source status consistency verified
    ↓
RFC-(N+1) may begin
```

The transition is incomplete if any required publication or verification step is missing.

## Fresh-state rule for every new project chat

Before making a statement about current RFC status, the assistant MUST:

1. restore relevant continuity from Arvectum OS project context;
2. read `docs/constitution/CONSTITUTION.md` from the current repository default branch;
3. read `docs/rfc/README.md` from the current repository default branch;
4. read the relevant RFC and approval decision records;
5. refresh the relevant canonical roadmap/planning artifact when status or next-step sequencing depends on it;
6. resolve discrepancies before characterizing the previous RFC as unapproved.

Previously fetched repository content, chat-local copies, model memory and prior roadmap snapshots MUST NOT be treated as current state.

## Discrepancy handling

If project continuity contains explicit owner approval but the repository still shows `Proposed`, treat this as an incomplete canonical publication transition.

The assistant MUST NOT simply report that the RFC "is still Proposed" without also checking for the later approval and incomplete publication state.

The required response is to restore the missing transition steps where safely possible, or explicitly identify the exact publication step that remains incomplete.

If the repository shows `Accepted` but an older roadmap snapshot shows `Proposed`, the repository's current canonical status prevails and the stale roadmap must be refreshed or synchronized.

## Read-after-write verification

After any RFC acceptance publication, the assistant MUST re-fetch the affected canonical files from the repository default branch rather than relying on the write response or pre-write content.

At minimum, verify consistency of:

- RFC document status/version;
- RFC Index status/version and approval evidence;
- owner approval decision record;
- canonical roadmap/planning state.

Substantive work on the next RFC starts only after these checks agree or an explicit discrepancy is surfaced.

## Relationship to higher-authority sources

This procedure is subordinate governance. It does not change:

- Constitution `1.2.0`;
- Accepted RFC architecture;
- the definition or normative force of RFC statuses;
- decision authority;
- RFC acceptance integrity requirements.

Where this procedure conflicts with a higher-authority canonical source, the higher-authority source prevails.
