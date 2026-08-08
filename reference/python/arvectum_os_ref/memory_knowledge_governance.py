"""P3.04 — bounded CAP-002 Memory & Knowledge Governance incubation slice.

Internal, in-memory, domain-neutral reference semantics only. This is not a
public API, durable knowledge store, vector contract, RAG framework or Active
Platform Capability.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum

from .canonical import CanonicalRecord
from .canonical_lineage import CanonicalLineage
from .identity import Identity
from .security import OrganizationScope

MEMORY_SEMANTIC_TYPE = "platform.memory"
KNOWLEDGE_SEMANTIC_TYPE = "platform.knowledge"


class MemoryKnowledgeGovernanceError(ValueError):
    pass


class KnowledgePromotionError(MemoryKnowledgeGovernanceError):
    pass


class KnowledgeRetrievalError(MemoryKnowledgeGovernanceError):
    pass


class LearningRole(str, Enum):
    OBSERVATION = "Observation"
    MEMORY = "Organizational Memory"
    CANDIDATE = "Knowledge Candidate"
    KNOWLEDGE = "Knowledge"


@dataclass(frozen=True, slots=True)
class KnowledgeConstraints:
    purpose: str
    classification: str
    rights: tuple[str, ...]
    freshness_state: str

    def __post_init__(self) -> None:
        if not all(isinstance(v, str) and v.strip() for v in (self.purpose, self.classification, self.freshness_state)):
            raise ValueError("purpose, classification and freshness_state must be explicit")
        if not self.rights or any(not isinstance(v, str) or not v.strip() for v in self.rights):
            raise ValueError("rights must be explicit")


@dataclass(frozen=True, slots=True)
class Observation:
    observation_id: Identity
    organization: OrganizationScope
    source_refs: tuple[Identity, ...]
    assertion: str

    def __post_init__(self) -> None:
        if not self.source_refs:
            raise ValueError("Observation requires attributable source evidence")
        if not self.assertion.strip():
            raise ValueError("Observation assertion must be explicit")


@dataclass(frozen=True, slots=True)
class MemoryItem:
    canonical_record: CanonicalRecord
    remembered_role: LearningRole
    source_refs: tuple[Identity, ...]
    constraints: KnowledgeConstraints

    def __post_init__(self) -> None:
        if self.canonical_record.semantic_type != MEMORY_SEMANTIC_TYPE:
            raise ValueError("Memory requires platform.memory Canonical Record semantics")
        if self.remembered_role is LearningRole.KNOWLEDGE:
            raise ValueError("Memory must not silently validate remembered material as Knowledge")
        if not self.source_refs:
            raise ValueError("Memory requires source attribution")


@dataclass(frozen=True, slots=True)
class KnowledgeCandidate:
    candidate_id: Identity
    organization: OrganizationScope
    subject_id: Identity
    proposition: str
    evidence_refs: tuple[Identity, ...]
    constraints: KnowledgeConstraints
    validation_result: str | None = None
    approval_ref: Identity | None = None

    def __post_init__(self) -> None:
        if not self.proposition.strip() or not self.evidence_refs:
            raise ValueError("candidate proposition and evidence must be explicit")


@dataclass(frozen=True, slots=True)
class ValidatedKnowledge:
    canonical_record: CanonicalRecord
    evidence_refs: tuple[Identity, ...]
    constraints: KnowledgeConstraints
    validation_result: str
    approval_ref: Identity

    @property
    def subject_id(self) -> Identity:
        return self.canonical_record.subject_id

    @property
    def version_id(self) -> Identity:
        return self.canonical_record.version_id


@dataclass(frozen=True, slots=True)
class RetrievalProjection:
    """Derived retrieval result; never canonical authority."""

    source_subject_id: Identity
    source_version_id: Identity
    summary: str
    ranking_score: float


@dataclass(frozen=True, slots=True)
class ExactKnowledgeReliance:
    subject_id: Identity
    version_id: Identity
    validation_result: str
    approval_ref: Identity


def record_validation(candidate: KnowledgeCandidate, *, result: str) -> KnowledgeCandidate:
    if not result.strip():
        raise ValueError("validation result must be explicit")
    return replace(candidate, validation_result=result)


def record_approval(candidate: KnowledgeCandidate, *, approval_ref: Identity) -> KnowledgeCandidate:
    return replace(candidate, approval_ref=approval_ref)


def promote_candidate(*, candidate: KnowledgeCandidate, canonical_record: CanonicalRecord) -> ValidatedKnowledge:
    """Promote only after distinct validation and approval evidence exists."""

    if canonical_record.semantic_type != KNOWLEDGE_SEMANTIC_TYPE:
        raise KnowledgePromotionError("promoted Knowledge must use platform.knowledge semantics")
    if canonical_record.organization != candidate.organization:
        raise KnowledgePromotionError("candidate and Knowledge must share Organization scope")
    if canonical_record.subject_id != candidate.subject_id:
        raise KnowledgePromotionError("candidate subject must match Knowledge subject")
    if not candidate.validation_result:
        raise KnowledgePromotionError("validation is required before Knowledge promotion")
    if candidate.approval_ref is None:
        raise KnowledgePromotionError("approval is distinct from validation and is required for this bounded promotion")
    return ValidatedKnowledge(
        canonical_record=canonical_record,
        evidence_refs=candidate.evidence_refs,
        constraints=candidate.constraints,
        validation_result=candidate.validation_result,
        approval_ref=candidate.approval_ref,
    )


def retrieve_eligible_knowledge(
    *,
    knowledge: tuple[ValidatedKnowledge, ...],
    organization: OrganizationScope,
    purpose: str,
    required_right: str,
    allow_stale: bool = False,
) -> tuple[RetrievalProjection, ...]:
    """Return bounded non-authoritative projections after governance filtering."""

    results: list[RetrievalProjection] = []
    for item in knowledge:
        if item.canonical_record.organization != organization:
            continue
        if item.constraints.purpose != purpose or required_right not in item.constraints.rights:
            continue
        if not allow_stale and item.constraints.freshness_state.lower() != "current":
            continue
        proposition = dict(item.canonical_record.payload).get("proposition", "")
        results.append(RetrievalProjection(item.subject_id, item.version_id, proposition, 1.0))
    return tuple(results)


def resolve_exact_knowledge_reliance(
    *,
    lineage: CanonicalLineage,
    validated: tuple[ValidatedKnowledge, ...],
    version_id: Identity,
) -> ExactKnowledgeReliance:
    """Resolve exact effective Knowledge Version; never rely on retrieval rank or Head inference."""

    exact = lineage.resolve_version(version_id)
    if exact.semantic_type != KNOWLEDGE_SEMANTIC_TYPE:
        raise KnowledgeRetrievalError("exact source is not validated Knowledge")
    matches = [item for item in validated if item.version_id == version_id and item.canonical_record == exact]
    if len(matches) != 1:
        raise KnowledgeRetrievalError("exact validated Knowledge Version is not uniquely resolvable")
    item = matches[0]
    return ExactKnowledgeReliance(item.subject_id, item.version_id, item.validation_result, item.approval_ref)
