# P6.05-L3 — Known Legacy Owner Classification

Status: `Prepared / owner-operated Mac diagnostic required`
Date: `2026-08-10`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operational environment: `Internal / local owner-operated runtime`
Production-readiness claim: `None`

## 1. Context

The fixed P6.05-L3 discovery manifest has seven verified `ai-corporation` checkouts and seven explicit env sources. Safe owner diagnostics proved that two env sources are repo-local, four are standalone non-Git sources, and one is untracked inside another valid Git repository whose origin is neither `ai-corporation` nor `arvectum-os`.

That result does not authorize migration from or mutation of the seventh source. Repository ownership is a security and operational boundary, and thematic similarity or common GitHub ownership is not sufficient authority.

## 2. Bounded next diagnostic

The available GitHub namespace contains two known historical procurement repositories that are materially closer to the current procurement lineage than arbitrary repositories:

- `arutyunoveth/tender-app`;
- `arutyunoveth/tender-ai`.

The helper `reference/python/p6_05_l3_classify_known_legacy_owner.py` classifies the unverified Git owner only into:

- `tender_app`;
- `tender_ai`;
- `same_account_other`;
- `external_other`;
- `no_origin`.

It does not emit a remote URL or path and does not claim that either known legacy repository is automatically an authorized secret source. A later bounded owner decision is still required before mutating an env in a repository outside the current verified `ai-corporation` checkout set.

## 3. Security properties

The helper uses only the existing local-only discovery manifest and Git metadata. It does not read env contents or secret values, calculate secret hashes, change permissions, rewrite files, create a destination, invoke a product, access EIS/SOAP, use the network, or perform any external action.

Any tracked env remains a hard stop. `same_account_other`, `external_other` and `no_origin` remain blocked and are not silently generalized into acceptable source categories.

## 4. Governance basis

Applicable authority remains Constitution `1.2.0` and Accepted RFC-0001/RFC-0003. RFC-0003 secret handling, minimization, least privilege and fail-closed requirements apply. No new RFC or ADR is required because this is a bounded, read-only, local diagnostic that creates no durable secret-management or repository-discovery contract.

## 5. Closure rule

This diagnostic does not complete P6.05-L3 and does not advance to L4. If the seventh source is classified as `tender_app` or `tender_ai` and remains untracked, a separate canonical owner-authorized migration decision must define whether that exact repository boundary may be modified. Other classifications remain blocked pending a different authority basis.
