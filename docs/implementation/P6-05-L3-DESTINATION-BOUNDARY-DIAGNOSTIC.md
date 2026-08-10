# P6.05-L3 — Destination boundary diagnostic

Status: internal bounded diagnostic for owner-operated local recovery.

## Context

The owner-authorized P6.05-L3 recovery may fail with `DESTINATION_INSIDE_SOURCE_CHECKOUT` before any legacy env or secret value is read. That failure means the intended external secret destination is contained by at least one verified source checkout boundary.

This diagnostic exists only to classify that boundary safely before choosing a corrected external location.

## Inputs

- the existing fixed P6.05-L3 discovery manifest;
- the intended destination path;
- expected checkout and env counts.

No rediscovery is performed.

## Safe output

The diagnostic reports only:

- verified source counts;
- whether the destination is contained by any supplied `ai-corporation` checkout;
- whether it is contained by the single already-identified `arutyunoveth/tender-app` owner;
- whether it is contained by the Arvectum OS checkout;
- whether another Git worktree owns the destination parent;
- whether no Git owner exists;
- whether the destination parent exists and is owner-only.

It does not emit paths, filenames, remote URLs, diffs or repository contents.

## Security boundary

The diagnostic MUST NOT:

- open or read any discovered env file;
- read a secret value;
- read the destination secret value;
- create, chmod, move, delete or rewrite any file;
- stage, commit, reset, stash or clean any repository;
- invoke a product, EIS/SOAP endpoint, network request or external action.

## Interpretation

A destination contained by a source checkout is not an acceptable L3 external secret boundary, even if the intended directory is untracked or ignored. The next correction must choose and independently verify a location outside every relevant Git checkout rather than weakening the containment rule.

This diagnostic does not select a new secret-management architecture, activate a Platform Capability or create a production deployment contract. Any relocation remains a bounded local implementation correction and must preserve RFC-0003 secret-handling requirements.
