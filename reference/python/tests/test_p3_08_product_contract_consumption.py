from dataclasses import replace
from datetime import datetime, timezone
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.document_artifact_governance import (
    ArtifactContent,
    DocumentVersionCandidate,
    HandlingConstraints,
    admit_document_version,
)
from arvectum_os_ref.event_provenance import ReconstructionManifest
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.governed_execution import GovernedGateKind
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.memory_knowledge_governance import KnowledgeConstraints, ValidatedKnowledge
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_002_MEMORY_KNOWLEDGE,
    CAP_003_SEARCH_PROJECTION,
    CAP_004_AUDIT_RECONSTRUCTION,
    CAPABILITY_CONTRACT_VERSION,
    OP_DISCOVER_SOURCES,
    OP_RECONSTRUCT_EXECUTION,
    OP_RESOLVE_DOCUMENT,
    OP_RESOLVE_SEARCH_SOURCE,
    OP_RETRIEVE_KNOWLEDGE,
    CapabilityConsumptionRequest,
    consume_document,
    consume_knowledge,
    consume_reconstruction,
    consume_search,
    consume_search_source,
    validate_capability_consumption,
)
from arvectum_os_ref.product_contract import (
    CanonicalAccessDeclaration,
    CanonicalAccessMode,
    HiddenProductPlatformCouplingError,
    PlatformDependencyDeclaration,
    ProductBoundaryMechanism,
    ProductContract,
    ProductContractCanonicalAccessError,
    ProductContractDependencyError,
    ProductContractLifecycle,
    ProductContractScopeError,
    ProductContractSecurityBoundaryError,
    ProductOperationDeclaration,
)
from arvectum_os_ref.search_index_projection import DiscoveryConstraints, GovernedSearchSource, rebuild_projection
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import OperationSideEffectClass


UTC = timezone.utc


class P308ProductContractConsumptionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.actor = ActorContext(Principal(self._id("principal", "consumer")), self.organization)
        self.access = AccessRequest(self.actor, "review", "read", ("internal",))
        self.product_id = self._id("product-experiment", "p3-08-bounded-consumer")
        self.contract = self._contract()

    def _id(self, namespace: str, value: str, scope: str = "org-a") -> Identity:
        return Identity(namespace, value, scope)

    def _time(self, minute: int = 0):
        return datetime(2026, 8, 8, 15, minute, tzinfo=UTC)

    def _record(self, *, subject: str, version: str, semantic_type: str, authority_scope: str | None = None, payload=()):
        return CanonicalRecord(
            subject_id=self._id("subject", subject),
            version_id=self._id("version", version),
            semantic_type=semantic_type,
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=authority_scope or f"{semantic_type}/state",
            accountable_owner_id=self.actor.actual_principal.principal_id,
            creation_actor=self.actor,
            created_at=self._time(),
            provenance_refs=(self.actor.actual_principal.principal_id,),
            integrity_metadata=(("representation", "p3.08-test"),),
            payload=payload,
            lifecycle_status="Retained",
        )

    def _dependency(self, dependency_id: Identity, operations: tuple[str, ...]) -> PlatformDependencyDeclaration:
        return PlatformDependencyDeclaration(
            dependency_id=dependency_id,
            contract_version=CAPABILITY_CONTRACT_VERSION,
            allowed_operations=operations,
            provider_responsibility="provide the bounded Incubating capability semantics",
            consumer_responsibility="use only the declared Product Contract and current access context",
            failure_behavior="fail closed without falling back to platform internals",
            provisional=True,
        )

    def _read(self, semantic_type: str) -> CanonicalAccessDeclaration:
        return CanonicalAccessDeclaration(
            semantic_type=semantic_type,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=f"{semantic_type}/state",
            access_modes=(CanonicalAccessMode.READ,),
            authoritative_source="Arvectum OS only within this bounded Native test authority scope",
            failure_behavior="reject undeclared canonical read",
        )

    def _operation(self, name: str, dependency_id: Identity, accesses=()) -> ProductOperationDeclaration:
        return ProductOperationDeclaration(
            operation_name=name,
            dependency_id=dependency_id,
            side_effect_classes=(OperationSideEffectClass.READ_ONLY,),
            required_gates=(GovernedGateKind.AUTHORIZATION, GovernedGateKind.DATA_GOVERNANCE),
            canonical_accesses=accesses,
            failure_behavior="fail closed without source disclosure or canonical mutation",
        )

    def _contract(self, *, lifecycle=ProductContractLifecycle.PROVISIONAL, operations=None, dependencies=None) -> ProductContract:
        owner = self.actor.actual_principal.principal_id
        record = CanonicalRecord(
            subject_id=self._id("product-contract-subject", "p3-08-bounded-consumer"),
            version_id=self._id("product-contract-version", "p3-08-bounded-consumer-v0.1.0"),
            semantic_type="platform.product-contract",
            schema_version="p3.08-internal-1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.product-contract/boundary",
            accountable_owner_id=owner,
            creation_actor=self.actor,
            created_at=self._time(),
            provenance_refs=(owner, self.product_id),
            integrity_metadata=(("representation", "bounded-reference-contract"),),
            payload=(("scope", "read-only consumption of CAP-001 through CAP-004"),),
            lifecycle_status=lifecycle.value,
        )
        default_dependencies = (
            self._dependency(CAP_001_DOCUMENT_ARTIFACT, (OP_RESOLVE_DOCUMENT,)),
            self._dependency(CAP_002_MEMORY_KNOWLEDGE, (OP_RETRIEVE_KNOWLEDGE,)),
            self._dependency(CAP_003_SEARCH_PROJECTION, (OP_DISCOVER_SOURCES, OP_RESOLVE_SEARCH_SOURCE)),
            self._dependency(CAP_004_AUDIT_RECONSTRUCTION, (OP_RECONSTRUCT_EXECUTION,)),
        )
        default_operations = (
            self._operation(OP_RESOLVE_DOCUMENT, CAP_001_DOCUMENT_ARTIFACT, (self._read("platform.document"),)),
            self._operation(OP_RETRIEVE_KNOWLEDGE, CAP_002_MEMORY_KNOWLEDGE, (self._read("platform.knowledge"),)),
            self._operation(OP_DISCOVER_SOURCES, CAP_003_SEARCH_PROJECTION),
            self._operation(OP_RESOLVE_SEARCH_SOURCE, CAP_003_SEARCH_PROJECTION, (self._read("platform.knowledge"),)),
            self._operation(OP_RECONSTRUCT_EXECUTION, CAP_004_AUDIT_RECONSTRUCTION),
        )
        return ProductContract(
            record=record,
            product_id=self.product_id,
            product_version="0.1.0",
            bounded_scope="one synthetic read-only Product Experiment consuming the four Phase 3 Incubating capabilities",
            compatibility_assumptions=(
                "Phase 3 Provisional capability contract baseline 1.0.0",
                "internal in-memory reference semantics only; no stable API or serialization",
            ),
            dependencies=default_dependencies if dependencies is None else dependencies,
            operations=default_operations if operations is None else operations,
            portability_responsibility="preserve exact governed identities/version references; derived views remain rebuildable",
            retention_deletion_responsibility="inherit current Organization source retention/deletion constraints",
            review_condition="review at P3.11 or earlier material capability-contract change",
            exit_path="revise, contain or retire; stabilization requires a separate RFC-0004 lifecycle decision",
        )

    def _request(
        self,
        dependency_id: Identity,
        operation_name: str,
        *,
        access: AccessRequest | None = None,
        dependency_contract_version: str = CAPABILITY_CONTRACT_VERSION,
        mechanism: ProductBoundaryMechanism = ProductBoundaryMechanism.DECLARED_PLATFORM_CONTRACT,
        organization: OrganizationScope | None = None,
        product_id: Identity | None = None,
    ) -> CapabilityConsumptionRequest:
        organization = self.organization if organization is None else organization
        return CapabilityConsumptionRequest(
            organization=organization,
            product_id=self.product_id if product_id is None else product_id,
            product_version="0.1.0",
            dependency_id=dependency_id,
            dependency_contract_version=dependency_contract_version,
            operation_name=operation_name,
            access=self.access if access is None else access,
            mechanism=mechanism,
        )

    def _document(self):
        record = self._record(subject="doc", version="doc-v1", semantic_type="platform.document")
        artifact = ArtifactContent(
            self._id("artifact", "a1"),
            self.organization,
            "content-ref",
            "text/plain",
            "sha256:x",
            "source",
            HandlingConstraints("internal", "review", ("read",), "retain"),
        )
        return admit_document_version(candidate=DocumentVersionCandidate(record, (artifact,), "source")), artifact

    def _knowledge(self):
        record = self._record(
            subject="knowledge", version="knowledge-v1", semantic_type="platform.knowledge",
            payload=(("proposition", "eligible"),),
        )
        return ValidatedKnowledge(
            record,
            (self._id("evidence", "e1"),),
            KnowledgeConstraints("review", "internal", ("read",), "Current"),
            "valid",
            self._id("approval", "a1"),
        )

    def _source(self):
        return GovernedSearchSource(
            self._record(
                subject="search-source",
                version="search-source-v1",
                semantic_type="platform.knowledge",
                payload=(("proposition", "needle"),),
            ),
            "needle",
            DiscoveryConstraints("review", "internal", ("read",), "retain"),
        )

    def _pin(self, role: str) -> GovernedVersionPin:
        return GovernedVersionPin(
            self._id(f"{role}-subject", role),
            self._id(f"{role}-version", f"{role}-v1"),
            f"example.{role}",
            f"{role}/state",
            "Retained",
        )

    def _manifest(self):
        workflow, material, execution, result, event = (
            self._pin(role) for role in ("workflow", "material", "execution", "result", "event")
        )
        execution_subject = self._id("execution-subject", "execution")
        manifest = ReconstructionManifest(
            organization=self.organization,
            execution_subject_id=execution_subject,
            initiating_actor_id=self.actor.actual_principal.principal_id,
            operation_name="review",
            workflow=workflow,
            material_inputs=(material,),
            gate_decisions=(),
            execution_versions=(execution,),
            results=(result,),
            events=(event,),
            event_types=(("example.event", "1"),),
            correlation_refs=(execution_subject,),
            causation_refs=(execution.version_id,),
            provenance_refs=(
                self.actor.actual_principal.principal_id,
                execution_subject,
                workflow.subject_id,
                workflow.version_id,
                material.subject_id,
                material.version_id,
                execution.subject_id,
                execution.version_id,
                result.subject_id,
                result.version_id,
                event.subject_id,
                event.version_id,
            ),
        )
        pins = (workflow, material, execution, result, event)
        constraints = tuple(
            (pin.version_id, "review", ("read",), "internal") for pin in pins
        )
        return manifest, constraints

    def test_bounded_consumer_uses_all_four_capabilities_through_contract(self) -> None:
        admitted, artifact = self._document()
        document = consume_document(
            contract=self.contract,
            request=self._request(CAP_001_DOCUMENT_ARTIFACT, OP_RESOLVE_DOCUMENT),
            admitted=admitted,
            artifact_id=artifact.artifact_id,
        )
        self.assertEqual(document.document_version_id, admitted.version_id)

        knowledge = self._knowledge()
        retrieved = consume_knowledge(
            contract=self.contract,
            request=self._request(CAP_002_MEMORY_KNOWLEDGE, OP_RETRIEVE_KNOWLEDGE),
            knowledge=(knowledge,),
        )
        self.assertEqual(tuple(item.source_version_id for item in retrieved), (knowledge.version_id,))

        source = self._source()
        projection = rebuild_projection(sources=(source,))
        hits = consume_search(
            contract=self.contract,
            request=self._request(CAP_003_SEARCH_PROJECTION, OP_DISCOVER_SOURCES),
            projection=projection,
            current_sources=(source,),
            query_text="needle",
        )
        self.assertEqual(len(hits), 1)
        resolved = consume_search_source(
            contract=self.contract,
            request=self._request(CAP_003_SEARCH_PROJECTION, OP_RESOLVE_SEARCH_SOURCE),
            hit=hits[0],
            current_sources=(source,),
        )
        self.assertEqual(resolved.version_id, source.version_id)

        manifest, constraints = self._manifest()
        view = consume_reconstruction(
            contract=self.contract,
            request=self._request(CAP_004_AUDIT_RECONSTRUCTION, OP_RECONSTRUCT_EXECUTION),
            manifest=manifest,
            evidence_constraints=constraints,
        )
        self.assertTrue(view.complete)

    def test_exact_product_contract_and_capability_versions_are_preserved(self) -> None:
        admission = validate_capability_consumption(
            contract=self.contract,
            request=self._request(CAP_001_DOCUMENT_ARTIFACT, OP_RESOLVE_DOCUMENT),
        )
        self.assertEqual(admission.product_contract_version_id, self.contract.record.version_id)
        self.assertEqual(admission.dependency_contract_version, CAPABILITY_CONTRACT_VERSION)
        self.assertTrue(all(item.provisional for item in self.contract.dependencies))
        self.assertEqual(self.contract.lifecycle, ProductContractLifecycle.PROVISIONAL)

    def test_undeclared_or_wrong_version_dependency_fails_closed(self) -> None:
        with self.assertRaises(ProductContractDependencyError):
            validate_capability_consumption(
                contract=self.contract,
                request=self._request(
                    Identity("platform-capability", "CAP-999", "platform"),
                    OP_RESOLVE_DOCUMENT,
                ),
            )
        with self.assertRaises(ProductContractDependencyError):
            validate_capability_consumption(
                contract=self.contract,
                request=self._request(
                    CAP_001_DOCUMENT_ARTIFACT,
                    OP_RESOLVE_DOCUMENT,
                    dependency_contract_version="2.0.0",
                ),
            )

    def test_hidden_platform_coupling_is_rejected(self) -> None:
        for mechanism in (
            ProductBoundaryMechanism.INTERNAL_TABLE,
            ProductBoundaryMechanism.INTERNAL_IMPORT,
            ProductBoundaryMechanism.UNDOCUMENTED_ENDPOINT,
            ProductBoundaryMechanism.PRIVATE_EVENT_STREAM,
            ProductBoundaryMechanism.IMPLICIT_SHARED_STATE,
        ):
            with self.subTest(mechanism=mechanism.value):
                with self.assertRaises(HiddenProductPlatformCouplingError):
                    validate_capability_consumption(
                        contract=self.contract,
                        request=self._request(
                            CAP_001_DOCUMENT_ARTIFACT,
                            OP_RESOLVE_DOCUMENT,
                            mechanism=mechanism,
                        ),
                    )

    def test_cross_organization_product_contract_reliance_is_rejected(self) -> None:
        org_b = OrganizationScope(Identity("organization", "org-b", "platform"))
        actor_b = ActorContext(Principal(Identity("principal", "consumer", "org-b")), org_b)
        access_b = AccessRequest(actor_b, "review", "read", ("internal",))
        with self.assertRaises(ProductContractScopeError):
            validate_capability_consumption(
                contract=self.contract,
                request=self._request(
                    CAP_001_DOCUMENT_ARTIFACT,
                    OP_RESOLVE_DOCUMENT,
                    organization=org_b,
                    product_id=Identity("product-experiment", "p3-08-bounded-consumer", "org-b"),
                    access=access_b,
                ),
            )

    def test_canonical_source_read_must_be_declared(self) -> None:
        operations = tuple(
            replace(item, canonical_accesses=())
            if item.operation_name == OP_RESOLVE_DOCUMENT
            else item
            for item in self.contract.operations
        )
        contract = self._contract(operations=operations)
        admitted, artifact = self._document()
        with self.assertRaises(ProductContractCanonicalAccessError):
            consume_document(
                contract=contract,
                request=self._request(CAP_001_DOCUMENT_ARTIFACT, OP_RESOLVE_DOCUMENT),
                admitted=admitted,
                artifact_id=artifact.artifact_id,
            )

    def test_authorization_and_data_governance_boundaries_cannot_be_dropped(self) -> None:
        operations = tuple(
            replace(item, required_gates=(GovernedGateKind.AUTHORIZATION,))
            if item.operation_name == OP_RETRIEVE_KNOWLEDGE
            else item
            for item in self.contract.operations
        )
        contract = self._contract(operations=operations)
        with self.assertRaises(ProductContractSecurityBoundaryError):
            validate_capability_consumption(
                contract=contract,
                request=self._request(CAP_002_MEMORY_KNOWLEDGE, OP_RETRIEVE_KNOWLEDGE),
            )

    def test_contract_and_admission_create_no_approval_or_organizational_authority(self) -> None:
        admission = validate_capability_consumption(
            contract=self.contract,
            request=self._request(CAP_004_AUDIT_RECONSTRUCTION, OP_RECONSTRUCT_EXECUTION),
        )
        for name in ("approve", "approval", "authority", "delegation", "permission"):
            self.assertFalse(hasattr(admission, name), name)
            self.assertFalse(hasattr(self.contract, name), name)

    def test_search_visibility_still_does_not_grant_source_access(self) -> None:
        source = self._source()
        projection = rebuild_projection(sources=(source,))
        denied_access = AccessRequest(self.actor, "review", "export", ("internal",))
        hits = consume_search(
            contract=self.contract,
            request=self._request(
                CAP_003_SEARCH_PROJECTION,
                OP_DISCOVER_SOURCES,
                access=denied_access,
            ),
            projection=projection,
            current_sources=(source,),
            query_text="needle",
        )
        self.assertEqual(hits, ())


if __name__ == "__main__":
    unittest.main()
