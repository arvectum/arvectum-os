# RFC State Transition Procedure

Status: `Approved`
Version: `1.1.0`
Effective: `2026-08-07`
Owner: `ООО «Арвектум»`
Category: `governance`
Approval evidence: `DECISION-2026-08-07-RFC-STATE-TRANSITION-CLOSURE`; `DECISION-2026-08-07-GITHUB-CONNECTOR-DISCOVERY`

## Purpose

Prevent stale RFC status from carrying across project chats, ensure that owner approval, canonical publication and roadmap state advance together, and prevent false claims that the canonical GitHub repository is unavailable merely because concrete connector operations have not yet been expanded in a new chat.

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

## Repository-access preflight for every new project chat

Before substantive Arvectum OS work, the assistant MUST establish current access to the canonical repository `arutyunoveth/arvectum-os`.

The assistant MUST NOT infer that GitHub is unavailable merely because concrete functions such as `fetch_file` are not already visible in the immediate chat tool context.

If the GitHub connector/resource is listed but the required operation is not directly exposed, the assistant MUST first perform connector discovery through the available connector gateway and discover an appropriate repository-read operation such as `fetch_file`, `fetch`, `search`, `get_repo` or an equivalent operation.

The required preflight is:

```text
Restore relevant project continuity
        ↓
Inspect available connectors/resources
        ↓
GitHub listed?
   ├─ yes → discover repository-read operation if needed
   │          ↓
   │       invoke it against arutyunoveth/arvectum-os
   │          ↓
   │       canonical repository read
   └─ no  → report connector absence accurately
```

A claim that the repository cannot be read, GitHub is unavailable, or the connector lacks repository-read capability is permitted only after an actual discovery/invocation attempt fails or the connector is genuinely absent from the available resource registry.

When one GitHub operation fails or is unavailable, the assistant SHOULD try another appropriate repository-read operation when doing so can distinguish an operation-level limitation from connector-level unavailability.

If repository access genuinely fails after the required attempt, the assistant MUST report the concrete failure condition and MUST NOT substitute remembered, chat-local or uploaded architecture as current canonical state.

## Fresh-state rule for every new project chat

After repository-access preflight succeeds and before making a statement about current RFC status, the assistant MUST:

1. restore relevant continuity from Arvectum OS project context;
2. read `docs/constitution/CONSTITUTION.md` from the current repository default branch;
3. read `docs/rfc/README.md` from the current repository default branch;
4. read the relevant RFC and approval decision records;
5. read relevant Accepted RFC and ADR required by task scope;
6. refresh the relevant canonical roadmap/planning artifact when status or next-step sequencing depends on it;
7. resolve discrepancies before characterizing the previous RFC as unapproved or the current task as blocked.

Previously fetched repository content, chat-local copies, uploaded copies, model memory and prior roadmap snapshots MUST NOT be treated as current state when live canonical repository access succeeds.

## Discrepancy handling

If project continuity contains explicit owner approval but the repository still shows `Proposed`, treat this as an incomplete canonical publication transition.

The assistant MUST NOT simply report that the RFC "is still Proposed" without also checking for the later approval and incomplete publication state.

The required response is to restore the missing transition steps where safely possible, or explicitly identify the exact publication step that remains incomplete.

If the repository shows `Accepted` but an older roadmap snapshot shows `Proposed`, the repository's current canonical status prevails and the stale roadmap must be refreshed or synchronized.

If project context and live repository state appear inconsistent, the assistant MUST distinguish:

- canonical repository state;
- project-chat continuity / owner intent;
- incomplete publication or synchronization work.

It MUST NOT collapse these into a false statement that an owner decision never occurred.

## Read-after-write verification

After any RFC acceptance publication or governance change affecting workflow state, the assistant MUST re-fetch the affected canonical files from the repository default branch rather than relying on the write response or pre-write content.

At minimum, for RFC acceptance verify consistency of:

- RFC document status/version;
- RFC Index status/version and approval evidence;
- owner approval decision record;
- canonical roadmap/planning state.

For changes to this governance procedure, verify the procedure file and its referenced approval decision from the default branch.

Substantive work on the next RFC starts only after these checks agree or an explicit discrepancy is surfaced.

## Relationship to higher-authority sources

This procedure is subordinate governance. It does not change:

- Constitution `1.2.0`;
- Accepted RFC architecture;
- the definition or normative force of RFC statuses;
- decision authority;
- RFC acceptance integrity requirements;
- canonical-source priority.

Where this procedure conflicts with a higher-authority canonical source, the higher-authority source prevails.
