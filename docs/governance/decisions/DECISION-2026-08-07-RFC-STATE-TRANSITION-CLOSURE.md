# DECISION-2026-08-07-RFC-STATE-TRANSITION-CLOSURE

Status: `Approved`
Date: `2026-08-07`
Owner: `ООО «Арвектум»`
Category: `governance`
Decision authority: owner of Arvectum OS

## Decision

For RFC work in Arvectum OS, an explicit owner approval is not considered operationally complete until the corresponding canonical state transition has been fully published and verified in the repository.

After an owner approves RFC-N, the working cycle MUST close the transition before work begins on RFC-(N+1):

1. record the owner approval as canonical decision evidence;
2. publish the approved RFC as `Accepted` with the appropriate accepted version;
3. synchronize `docs/rfc/README.md`;
4. synchronize the canonical roadmap or equivalent planning artifact;
5. re-read the repository default branch after the writes and verify that all canonical status surfaces agree;
6. only then begin substantive work on the next RFC.

A new project chat MUST NOT rely on a previously read roadmap, RFC Index, model memory, chat-local snapshot or cached repository state as evidence of current RFC status. It MUST restore relevant project continuity first and then refresh canonical state from the repository default branch.

If project continuity contains a later explicit owner approval than the repository currently reflects, the discrepancy MUST be treated as an incomplete publication transition, not as evidence that the owner failed to approve. The assistant MUST repair or surface the incomplete canonical transition before using the stale repository status to characterize the prior RFC.

## Rationale

The prior workflow allowed owner approval to be captured in one chat while publication of `Accepted` status, RFC Index synchronization or roadmap synchronization remained incomplete. The next chat then correctly read the repository but incorrectly described the owner's previously approved RFC as merely `Proposed`. Repeating this pattern creates a one-step lag in perceived governance state.

This procedure makes approval publication transactional from the perspective of task progression and introduces mandatory read-after-write verification.

## Scope

This decision changes governance workflow only. It does not alter the Constitution, Accepted architectural RFC semantics, RFC acceptance integrity requirements, decision authority, or the normative meaning of RFC statuses.

## Provenance

This decision records the owner's explicit directive on 2026-08-07 to correct the recurring one-step status lag between consecutive RFC task chats. It is a current governance repair decision and does not fabricate historical approval evidence.
