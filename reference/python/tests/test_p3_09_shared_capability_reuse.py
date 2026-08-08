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
)
from arvectum_os_ref.product_contract import (
    CanonicalAccessDeclaration,
    CanonicalAccessMode,
    PlatformDependencyDeclaration,
    ProductContract,
    ProductContractCanonicalAccessError,
    ProductContractLifecycle,
    ProductOperationDeclaration,
)
from arvectum_os_ref.search_index_projection import (
    DiscoveryConstraints,
    GovernedSearchSource,
    rebuild_projection,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.shared_capability_reuse import (
    BoundedConsumerComposition,
    SharedCapabilityReuseError,
    prove_shared_capability_reuse,
)
from arvectum_os_ref.workflow import OperationSideEffectClass


UTC = timezone.utc


class P309SharedCapabilityReuseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.actor_a = ActorContext(Principal(self._id("principal", "consumer-a")), self.organization)
        self.actor_b = ActorContext(Principal(self._id("principal", "consumer-b")), self.organization)
        self.access_a = AccessRequest(self.actor_a, "review", "read", ("internal",))
        self.access_b = AccessRequest(self.actor_b, "triage", "read", ("internal",))
        self.product_a = self._id("product-experiment", "p3-08-bounded-consumer")
        self.product_b = self._id("product-experiment", "p3-09-distinct-consumer")
        self.contract_a = self._contract(
            product_id=self.product_a,
            product_version="0.1.0",
            name="p3-08-bounded-consumer",
            actor=self.actor_a,
            search_source_semantic_type="platform.knowledge",
        )
        self.contract_b = self._contract(
            product_id=self.product_b,
            product_version="0.1.0",
            name="p3-09-distinct-consumer",
            actor=self.actor_b,
            search_source_semantic_type="platform.document",
        )
        self.workflow_a = self._workflow("document-led-review", "workflow-a-v1")
        self.workflow_b = self._workflow("discovery-led-triage", "workflow-b-v1")

    def _id(self, namespace: str, value: str, scope: str = "org-a") -> Identity:
        return Identity(namespace, value, scope)

    def _record(
        self,
        subject: str,
        version: str,
        semantic_type: str,
        *,
        actor: ActorContext,
        payload=(),
    ) -> CanonicalRecord:
        return CanonicalRecord(
            subject_id=self._id("subject", subject),
            version_id=self._id("version", version),
            semantic_type=semantic_type,
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=f"{semantic_type}/state",
            accountable_owner_id=actor.actual_principal.principal_id,
            creation_actor=actor,
            created_at=datetime(2026, 8, 8, 17, 0, tzinfo=UTC),
            provenance_refs=(actor.actual_principal.principal_id,),
            integrity_metadata=(("representation", "p3.09-test"),),
            payload=payload,
            lifecycle_status="Retained",
        )

    def _dependency(self, dependency_id: Identity, operations: tuple[str, ...]) -> PlatformDependencyDeclaration:
        return PlatformDependencyDeclaration(
            dependency_id=dependency_id,
            contract_version=CAPABILITY_CONTRACT_VERSION,
            allowed_operations=operations,
            provider_responsibility="provide bounded Incubating capability semantics unchanged across consumers",
            consumer_responsibility="compose only declared Product Contract operations and current access context",
            failure_behavior="fail closed without platform-internal fallback",
            provisional=True,
        )

    def _read(self, semantic_type: str) -> CanonicalAccessDeclaration:
        return CanonicalAccessDeclaration(
            semantic_type=semantic_type,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=f"{semantic_type}/state",
            access_modes=(CanonicalAccessMode.READ,),
            authoritative_source="Arvectum OS inside the bounded Native fixture scope",
            failure_behavior="reject undeclared canonical read",
        )

    def _operation(self, name: str, dependency_id: Identity, *, accesses=()) -> ProductOperationDeclaration:
        return ProductOperationDeclaration(
            operation_name=name,
            dependency_id=dependency_id,
            side_effect_classes=(OperationSideEffectClass.READ_ONLY,),
            required_gates=(
                GovernedGateKind.AUTHORIZATION,
                GovernedGateKind.DATA_GOVERNANCE,
            ),
            canonical_accesses=accesses,
            failure_behavior="fail closed without source disclosure or canonical mutation",
        )

    def _contract(
        self,
        *,
        product_id: Identity,
        product_version: str,
        name: str,
        actor: ActorContext,
        search_source_semantic_type: str,
    ) -> ProductContract:
        owner = actor.actual_principal.principal_id
        record = CanonicalRecord(
            subject_id=self._id("product-contract-subject", name),
            version_id=self._id("product-contract-version", f"{name}-v{product_version}"),
            semantic_type="platform.product-contract",
            schema_version="p3.09-internal-1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.product-contract/boundary",
            accountable_owner_id=owner,
            creation_actor=actor,
            created_at=datetime(2026, 8, 8, 17, 0, tzinfo=UTC),
            provenance_refs=(owner, product_id),
            integrity_metadata=(("representation", "bounded-reference-contract"),),
            payload=(("scope", "read-only cross-consumer reuse of CAP-001 through CAP-004"),),
            lifecycle_status=ProductContractLifecycle.PROVISIONAL.value,
        )
        dependencies = (
            self._dependency(CAP_001_DOCUMENT_ARTIFACT, (OP_RESOLVE_DOCUMENT,)),
            self._dependency(CAP_002_MEMORY_KNOWLEDGE, (OP_RETRIEVE_KNOWLEDGE,)),
            self._dependency(
                CAP_003_SEARCH_PROJECTION,
                (OP_DISCOVER_SOURCES, OP_RESOLVE_SEARCH_SOURCE),
            ),
            self._dependency(CAP_004_AUDIT_RECONSTRUCTION, (OP_RECONSTRUCT_EXECUTION,)),
        )
        operations = (
            self._operation(
                OP_RESOLVE_DOCUMENT,
                CAP_001_DOCUMENT_ARTIFACT,
                accesses=(self._read("platform.document"),),
            ),
            self._operation(
                OP_RETRIEVE_KNOWLEDGE,
                CAP_002_MEMORY_KNOWLEDGE,
                accesses=(self._read("platform.knowledge"),),
            ),
            self._operation(OP_DISCOVER_SOURCES, CAP_003_SEARCH_PROJECTION),
            self._operation(
                OP_RESOLVE_SEARCH_SOURCE,
                CAP_003_SEARCH_PROJECTION,
                accesses=(self._read(search_source_semantic_type),),
            ),
            self._operation(OP_RECONSTRUCT_EXECUTION, CAP_004_AUDIT_RECONSTRUCTION),
        )
        return ProductContract(
            record=record,
            product_id=product_id,
            product_version=product_version,
            bounded_scope="one synthetic read-only consumer composition over CAP-001 through CAP-004",
            compatibility_assumptions=(
                "Phase 3 Provisional capability contract baseline 1.0.0",
                "internal in-memory reference semantics only",
            ),
            dependencies=dependencies,
            operations=operations,
            portability_responsibility="preserve governed identities and exact version references",
            retention_deletion_responsibility="inherit applicable Organization source rules",
            review_condition="P3.11 or earlier material capability-contract change",
            exit_path="revise, contain or retire; stabilization requires a separate lifecycle decision",
        )

    def _workflow(self, subject: str, version: str) -> GovernedVersionPin:
        return GovernedVersionPin(
            self._id("workflow-subject", subject),
            self._id("workflow-version", version),
            "platform.workflow",
            "platform.workflow/definition",
            "Retained",
        )

    def _request(
        self,
        *,
        product_id: Identity,
        product_version: str,
        access: AccessRequest,
        dependency_id: Identity,
        operation_name: str,
    ) -> CapabilityConsumptionRequest:
        return CapabilityConsumptionRequest(
            organization=self.organization,
            product_id=product_id,
            product_version=product_version,
            dependency_id=dependency_id,
            dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
            operation_name=operation_name,
            access=access,
        )

    def _composition_a(self) -> BoundedConsumerComposition:
        ordered = (
            (CAP_001_DOCUMENT_ARTIFACT, OP_RESOLVE_DOCUMENT),
            (CAP_002_MEMORY_KNOWLEDGE, OP_RETRIEVE_KNOWLEDGE),
            (CAP_003_SEARCH_PROJECTION, OP_DISCOVER_SOURCES),
            (CAP_003_SEARCH_PROJECTION, OP_RESOLVE_SEARCH_SOURCE),
            (CAP_004_AUDIT_RECONSTRUCTION, OP_RECONSTRUCT_EXECUTION),
        )
        return BoundedConsumerComposition(
            self.workflow_a,
            tuple(
                self._request(
                    product_id=self.product_a,
                    product_version="0.1.0",
                    access=self.access_a,
                    dependency_id=dependency_id,
                    operation_name=operation_name,
                )
                for dependency_id, operation_name in ordered
            ),
        )

    def _composition_b(self) -> BoundedConsumerComposition:
        ordered = (
            (CAP_003_SEARCH_PROJECTION, OP_DISCOVER_SOURCES),
            (CAP_003_SEARCH_PROJECTION, OP_RESOLVE_SEARCH_SOURCE),
            (CAP_001_DOCUMENT_ARTIFACT, OP_RESOLVE_DOCUMENT),
            (CAP_004_AUDIT_RECONSTRUCTION, OP_RECONSTRUCT_EXECUTION),
            (CAP_002_MEMORY_KNOWLEDGE, OP_RETRIEVE_KNOWLEDGE),
        )
        return BoundedConsumerComposition(
            self.workflow_b,
            tuple(
                self._request(
                    product_id=self.product_b,
                    product_version="0.1.0",
                    access=self.access_b,
                    dependency_id=dependency_id,
                    operation_name=operation_name,
                )
                for dependency_id, operation_name in ordered
            ),
        )

    def _request_for(self, composition: BoundedConsumerComposition, operation_name: str):
        matches = tuple(item for item in composition.requests if item.operation_name == operation_name)
        self.assertEqual(len(matches), 1)
        return matches[0]

    def _document(self, *, actor: ActorContext, purpose: str, name: str):
        record = self._record(name, f"{name}-v1", "platform.document", actor=actor)
        artifact = ArtifactContent(
            self._id("artifact", f"{name}-artifact"),
            self.organization,
            f"content-ref:{name}",
            "text/plain",
            f"sha256:{name}",
            "source",
            HandlingConstraints("internal", purpose, ("read",), "retain"),
        )
        return admit_document_version(candidate=DocumentVersionCandidate(record, (artifact,), "source")), artifact

    def _knowledge(self, *, actor: ActorContext, purpose: str, name: str) -> ValidatedKnowledge:
        record = self._record(
            name,
            f"{name}-v1",
            "platform.knowledge",
            actor=actor,
            payload=(("proposition", f"{name} eligible"),),
        )
        return ValidatedKnowledge(
            record,
            (self._id("evidence", f"{name}-e1"),),
            KnowledgeConstraints(purpose, "internal", ("read",), "Current"),
            "valid",
            self._id("approval", f"{name}-a1"),
        )

    def _search_source(self, *, record: CanonicalRecord, purpose: str, text: str) -> GovernedSearchSource:
        return GovernedSearchSource(
            record,
            text,
            DiscoveryConstraints(purpose, "internal", ("read",), "retain"),
        )

    def _pin(self, role: str, suffix: str) -> GovernedVersionPin:
        return GovernedVersionPin(
            self._id(f"{role}-subject", f"{role}-{suffix}"),
            self._id(f"{role}-version", f"{role}-{suffix}-v1"),
            f"example.{role}",
            f"{role}/state",
            "Retained",
        )

    def _manifest(self, *, actor: ActorContext, suffix: str):
        workflow, material, execution, result, event = (
            self._pin(role, suffix) for role in ("workflow-evidence", "material", "execution", "result", "event")
        )
        execution_subject = self._id("execution-subject", f"execution-{suffix}")
        manifest = ReconstructionManifest(
            organization=self.organization,
            execution_subject_id=execution_subject,
            initiating_actor_id=actor.actual_principal.principal_id,
            operation_name=f"read-{suffix}",
            workflow=workflow,
            material_inputs=(material,),
            gate_decisions=(),
            execution_versions=(execution,),
            results=(result,),
            events=(event,),
            event_types=(("example.event", "1"),),
            correlation_refs=(execution_subject,),
            causation_refs=(execution.version_id,),
            provenance_refs=tuple(dict.fromkeys((
                actor.actual_principal.principal_id,
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
            ))),
        )
        constraints = tuple(
            (pin.version_id, "review" if suffix == "a" else "triage", ("read",), "internal")
            for pin in (workflow, material, execution, result, event)
        )
        return manifest, constraints

    def test_two_materially_distinct_consumers_reuse_all_four_capabilities(self) -> None:
        first = self._composition_a()
        second = self._composition_b()
        proof = prove_shared_capability_reuse(
            first_contract=self.contract_a,
            first_composition=first,
            second_contract=self.contract_b,
            second_composition=second,
        )

        self.assertEqual(
            proof.shared_capability_ids,
            (
                CAP_001_DOCUMENT_ARTIFACT,
                CAP_002_MEMORY_KNOWLEDGE,
                CAP_003_SEARCH_PROJECTION,
                CAP_004_AUDIT_RECONSTRUCTION,
            ),
        )
        self.assertEqual(proof.capability_contract_version, CAPABILITY_CONTRACT_VERSION)
        self.assertNotEqual(proof.first_product_id, proof.second_product_id)
        self.assertNotEqual(proof.first_product_contract_version_id, proof.second_product_contract_version_id)
        self.assertNotEqual(proof.first_workflow_version_id, proof.second_workflow_version_id)
        self.assertNotEqual(proof.first_operation_signature, proof.second_operation_signature)
        self.assertEqual(len(proof.admissions), 10)
        self.assertTrue(all(not hasattr(item, "authorization") for item in proof.admissions))
        self.assertTrue(all(not hasattr(item, "organizational_authority") for item in proof.admissions))
        self.assertIs(self.contract_a.lifecycle, ProductContractLifecycle.PROVISIONAL)
        self.assertIs(self.contract_b.lifecycle, ProductContractLifecycle.PROVISIONAL)

    def test_document_led_consumer_executes_without_platform_semantic_special_case(self) -> None:
        composition = self._composition_a()
        admitted, artifact = self._document(actor=self.actor_a, purpose="review", name="doc-a")
        knowledge = self._knowledge(actor=self.actor_a, purpose="review", name="knowledge-a")
        source = self._search_source(record=knowledge.canonical_record, purpose="review", text="needle knowledge")
        projection = rebuild_projection(sources=(source,))
        manifest, constraints = self._manifest(actor=self.actor_a, suffix="a")

        document = consume_document(
            contract=self.contract_a,
            request=self._request_for(composition, OP_RESOLVE_DOCUMENT),
            admitted=admitted,
            artifact_id=artifact.artifact_id,
        )
        retrieved = consume_knowledge(
            contract=self.contract_a,
            request=self._request_for(composition, OP_RETRIEVE_KNOWLEDGE),
            knowledge=(knowledge,),
        )
        hits = consume_search(
            contract=self.contract_a,
            request=self._request_for(composition, OP_DISCOVER_SOURCES),
            projection=projection,
            current_sources=(source,),
            query_text="needle",
        )
        resolved = consume_search_source(
            contract=self.contract_a,
            request=self._request_for(composition, OP_RESOLVE_SEARCH_SOURCE),
            hit=hits[0],
            current_sources=(source,),
        )
        reconstruction = consume_reconstruction(
            contract=self.contract_a,
            request=self._request_for(composition, OP_RECONSTRUCT_EXECUTION),
            manifest=manifest,
            evidence_constraints=constraints,
        )

        self.assertEqual(document.document_version_id, admitted.version_id)
        self.assertEqual(tuple(item.source_version_id for item in retrieved), (knowledge.version_id,))
        self.assertEqual(resolved.version_id, knowledge.version_id)
        self.assertTrue(reconstruction.complete)

    def test_discovery_led_consumer_reuses_same_capabilities_over_document_source(self) -> None:
        composition = self._composition_b()
        admitted, artifact = self._document(actor=self.actor_b, purpose="triage", name="doc-b")
        knowledge = self._knowledge(actor=self.actor_b, purpose="triage", name="knowledge-b")
        source = self._search_source(record=admitted.canonical_record, purpose="triage", text="needle document")
        projection = rebuild_projection(sources=(source,))
        manifest, constraints = self._manifest(actor=self.actor_b, suffix="b")

        hits = consume_search(
            contract=self.contract_b,
            request=self._request_for(composition, OP_DISCOVER_SOURCES),
            projection=projection,
            current_sources=(source,),
            query_text="needle",
        )
        resolved = consume_search_source(
            contract=self.contract_b,
            request=self._request_for(composition, OP_RESOLVE_SEARCH_SOURCE),
            hit=hits[0],
            current_sources=(source,),
        )
        document = consume_document(
            contract=self.contract_b,
            request=self._request_for(composition, OP_RESOLVE_DOCUMENT),
            admitted=admitted,
            artifact_id=artifact.artifact_id,
        )
        reconstruction = consume_reconstruction(
            contract=self.contract_b,
            request=self._request_for(composition, OP_RECONSTRUCT_EXECUTION),
            manifest=manifest,
            evidence_constraints=constraints,
        )
        retrieved = consume_knowledge(
            contract=self.contract_b,
            request=self._request_for(composition, OP_RETRIEVE_KNOWLEDGE),
            knowledge=(knowledge,),
        )

        self.assertEqual(resolved.version_id, admitted.version_id)
        self.assertEqual(document.document_version_id, admitted.version_id)
        self.assertTrue(reconstruction.complete)
        self.assertEqual(tuple(item.source_version_id for item in retrieved), (knowledge.version_id,))

    def test_second_consumer_cannot_borrow_first_consumer_contract(self) -> None:
        with self.assertRaises(SharedCapabilityReuseError):
            prove_shared_capability_reuse(
                first_contract=self.contract_a,
                first_composition=self._composition_a(),
                second_contract=self.contract_a,
                second_composition=self._composition_b(),
            )

    def test_identical_composition_order_is_not_materially_distinct_evidence(self) -> None:
        second_requests = tuple(
            self._request(
                product_id=self.product_b,
                product_version="0.1.0",
                access=self.access_b,
                dependency_id=item.dependency_id,
                operation_name=item.operation_name,
            )
            for item in self._composition_a().requests
        )
        duplicated_shape = BoundedConsumerComposition(self.workflow_b, second_requests)
        with self.assertRaises(SharedCapabilityReuseError):
            prove_shared_capability_reuse(
                first_contract=self.contract_a,
                first_composition=self._composition_a(),
                second_contract=self.contract_b,
                second_composition=duplicated_shape,
            )

    def test_missing_shared_operation_is_not_reuse_proof(self) -> None:
        incomplete = BoundedConsumerComposition(
            self.workflow_b,
            tuple(
                item for item in self._composition_b().requests
                if item.operation_name != OP_RECONSTRUCT_EXECUTION
            ),
        )
        with self.assertRaises(SharedCapabilityReuseError):
            prove_shared_capability_reuse(
                first_contract=self.contract_a,
                first_composition=self._composition_a(),
                second_contract=self.contract_b,
                second_composition=incomplete,
            )

    def test_consumer_specific_source_read_does_not_bleed_into_other_contract(self) -> None:
        composition = self._composition_a()
        admitted, _ = self._document(actor=self.actor_a, purpose="review", name="doc-isolated")
        source = self._search_source(record=admitted.canonical_record, purpose="review", text="needle document")
        projection = rebuild_projection(sources=(source,))
        hits = consume_search(
            contract=self.contract_a,
            request=self._request_for(composition, OP_DISCOVER_SOURCES),
            projection=projection,
            current_sources=(source,),
            query_text="needle",
        )
        self.assertEqual(len(hits), 1)
        with self.assertRaises(ProductContractCanonicalAccessError):
            consume_search_source(
                contract=self.contract_a,
                request=self._request_for(composition, OP_RESOLVE_SEARCH_SOURCE),
                hit=hits[0],
                current_sources=(source,),
            )

    def test_capability_contract_version_cannot_be_broadened_for_second_consumer(self) -> None:
        second = self._composition_b()
        altered = BoundedConsumerComposition(
            self.workflow_b,
            tuple(
                replace(item, dependency_contract_version="2.0.0")
                if item.operation_name == OP_RETRIEVE_KNOWLEDGE
                else item
                for item in second.requests
            ),
        )
        with self.assertRaises(SharedCapabilityReuseError):
            prove_shared_capability_reuse(
                first_contract=self.contract_a,
                first_composition=self._composition_a(),
                second_contract=self.contract_b,
                second_composition=altered,
            )


if __name__ == "__main__":
    unittest.main()
