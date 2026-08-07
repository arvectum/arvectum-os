# DECISION-2026-08-07: GitHub Connector Discovery Before Repository-Unavailable Claims

Status: `Approved`
Date: `2026-08-07`
Owner / decision authority: `ООО «Арвектум»`
Category: `governance`
Scope: Arvectum OS project-chat repository access

## Decision

For every Arvectum OS project chat, the assistant MUST treat the configured GitHub connector as potentially usable even when concrete GitHub operations are not yet expanded into the immediate tool context.

Before stating or implying that the canonical repository `arutyunoveth/arvectum-os` cannot be read, is unavailable, or that GitHub access is absent, the assistant MUST perform connector discovery and an actual repository read attempt.

The mandatory sequence is:

1. inspect the available connector/resource registry for `GitHub`;
2. if GitHub is listed but concrete operations are not directly visible, discover the relevant operation through the connector gateway (for example `fetch_file`, `fetch`, `search`, `get_repo` or an equivalent repository-read operation);
3. invoke the discovered GitHub operation against the canonical repository;
4. only after a real connector/discovery/invocation failure may repository access be described as unavailable;
5. when one GitHub operation is unavailable, try another appropriate repository-read operation when doing so can distinguish operation-level failure from connector-level failure.

The absence of an already-expanded `GitHub.fetch_file` function in the immediate chat context MUST NOT be interpreted as absence of GitHub access.

## New-chat preflight

For substantive Arvectum OS work, a new project chat MUST execute the following repository preflight before architecture/governance conclusions:

```text
Project context continuity
        ↓
GitHub connector discovery (when needed)
        ↓
Canonical repository read succeeds
        ↓
Constitution
        ↓
RFC Index
        ↓
Relevant Accepted RFC / ADR / governance artifacts
        ↓
Substantive work
```

If repository access genuinely fails after discovery and invocation, the assistant MUST report the concrete failure condition and MUST NOT substitute remembered architecture as canonical state.

## Rationale

GitHub connector functions may be lazily exposed per chat. A new chat can therefore see the GitHub connector without yet seeing individual operations. Treating this lazy exposure as missing access creates false repository-unavailable claims and breaks mandatory repository lookup and project continuity.

## Consequences

- New chats must discover GitHub operations before concluding that repository access is unavailable.
- Tool discovery becomes part of the Arvectum OS repository preflight.
- Claims about unavailable canonical state require evidence from an actual connector attempt.
- Chat memory, uploaded copies and prior repository snapshots remain fallback context only and do not replace current canonical repository lookup when the connector works.

## Relationship to existing governance

This decision extends the operational procedure for fresh-state checks and cross-chat continuity. It does not modify Constitution, Accepted RFC architecture, decision authority, RFC acceptance semantics or canonical-source priority.
