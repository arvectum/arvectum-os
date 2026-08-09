from datetime import datetime, timezone
import unittest

from arvectum_os_ref.audit_reconstruction_support import EvidenceAvailability
from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord, ExternalAuthorityContract
from arvectum_os_ref.cross_capability_enforcement import AccessRequest, CrossCapabilityEnforcementError
from arvectum_os_ref.document_artifact_governance import (
    ArtifactContent,
    DocumentVersionCandidate,
    HandlingConstraints,
    admit_document_version,
)
from arvectum_os_ref.event_provenance import ReconstructionManifest
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.integration_adapters import compose_integration_adapters
from arvectum_os_ref.integration_composition import IntegrationCompositionEvidenceRequiredError
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_002_MEMORY_KNOWLEDGE,
    CAP_003_SEARCH_PROJECTION,
    CAP_004_AUDIT_RECONSTRUCTION,
    CAPABILITY_CONTRACT_VERSION,
    OP_RECONSTRUCT_EXECUTION,
    OP_RESOLVE_DOCUMENT,
    CapabilityConsumptionRequest,
)
from arvectum_os_ref.product_contract import (
    HiddenProductPlatformCouplingError,
    ProductBoundaryMechanism,
    ProductContractScopeError,
)
from arvectum_os_ref.product_contract_resolution import (
    DependencySupportDisposition,
    DeprecatedDependencyResolutionError,
    GovernedDependencyVersionEvidence,
    IncompatibleDependencyVersionError,
    UnsupportedDependencyResolutionError,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import OperationSideEffectClass
from p6_03_tender_operator_ref.contract import (
    DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
    PRODUCT_COMPATIBILITY_LINE,
    PRODUCT_CONTRACT_VERSION,
    build_p6_02_product_contract,
)


UTC = timezone.utc


class P603FirstRealProductIntegrationStage1Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "p6-03-org-a", "platform"))
        self.actor = ActorContext(
            Principal(Identity("principal", "p6-03-operator", "p6-03-org-a")),
            self.organization,
        )
        self.created_at = datetime(2026, 8, 9, 16, 0, tzinfo=UTC)
        self.contract = build_p6_02_product_contract(actor=self.actor, created_at=self.created_at)
        self.access = AccessRequest(
            self.actor,
            "prebid-review",
            "read",
            ("restricted-pilot",),
        )
        self.governed_versions = self._supported_versions()
        self.adapters = compose_integration_adapters(
            contract=self.contract,
            actor=self.actor,
            effective_product_contract=self.contract.version_pin,
            governed_versions=self.governed_versions,
        )

    def _id(self, namespace: str, value: str, scope: str = "p6-03-org-a") -> Identity:
        return Identity(namespace, value, scope)

    def _supported_versions(self):
        governance = "docs/contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md@1.0.0"
        return (
            GovernedDependencyVersionEvidence(
                CAP_001_DOCUMENT_ARTIFACT,
                CAPABILITY_CONTRACT_VERSION,
                DependencySupportDisposition.SUPPORTED,
                governance,
            ),
            GovernedDependencyVersionEvidence(
                CAP_004_AUDIT_RECONSTRUCTION,
                CAPABILITY_CONTRACT_VERSION,
                DependencySupportDisposition.SUPPORTED,
                governance,
            ),
        )

    def _request(
        self,
        dependency_id: Identity,
        operation_name: str,
        *,
        access: AccessRequest | None = None,
        organization: OrganizationScope | None = None,
        product_id: Identity | None = None,
        dependency_version: str = CAPABILITY_CONTRACT_VERSION,
        mechanism: ProductBoundaryMechanism = ProductBoundaryMechanism.DECLARED_PLATFORM_CONTRACT,
    ) -> CapabilityConsumptionRequest:
        organization = self.organization if organization is None else organization
        return CapabilityConsumptionRequest(
            organization=organization,
            product_id=self.contract.product_id if product_id is None else product_id,
            product_version=PRODUCT_COMPATIBILITY_LINE,
            dependency_id=dependency_id,
            dependency_contract_version=dependency_version,
            operation_name=operation_name,
            access=self.access if access is None else access,
            mechanism=mechanism,
        )

    def _external_document(self):
        authority = ExternalAuthorityContract(
            authoritative_system="synthetic-redacted-eis-source",
            external_object_ref="redacted:44fz:case-001:document-001",
            authority_scope=DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
            retrieval_or_sync="reference-only controlled retrieval; no authoritative local synchronization",
            freshness_expectation="exact accepted source package used by this synthetic Stage 1 run",
            source_version_semantics="source package digest plus explicit retrieval provenance",
            conflict_rule="external source remains authoritative; local mismatch fails closed",
            failure_behavior="source/reference unavailability blocks governed reliance; no cached authority fallback",
            permitted_transformations=("redaction", "integrity hashing"),
            retention_deletion="inherit approved source retention/deletion constraints",
            portability="export the governed reference/provenance without requiring source credentials",
        )
        record = CanonicalRecord(
            subject_id=self._id("document-subject", "redacted-tender-document"),
            version_id=self._id("document-version", "redacted-tender-document-v1"),
            semantic_type="platform.document",
            schema_version="p6.03-stage1-1",
            organization=self.organization,
            authority_mode=AuthorityMode.EXTERNAL_REFERENCE,
            authority_scope=DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
            accountable_owner_id=self.actor.actual_principal.principal_id,
            creation_actor=self.actor,
            created_at=self.created_at,
            provenance_refs=(self.actor.actual_principal.principal_id,),
            integrity_metadata=(("fixture", "synthetic-redacted-no-real-tender-content"),),
            payload=(("source", "synthetic-redacted-external-reference"),),
            lifecycle_status="AdmittedReference",
            external_authority=authority,
        )
        artifact = ArtifactContent(
            artifact_id=self._id("artifact", "redacted-tender-document-artifact-v1"),
            organization=self.organization,
            content_ref="redacted://p6.03/tender/document-001",
            media_type="application/pdf",
            integrity_ref="sha256:synthetic-redacted-document-v1",
            rendition_role="source",
            handling=HandlingConstraints(
                "restricted-pilot",
                "prebid-review",
                ("read",),
                "synthetic-stage1-only",
            ),
        )
        admitted = admit_document_version(
            DocumentVersionCandidate(record, (artifact,), "source")
        )
        return admitted, artifact

    def _pin(self, namespace: str, value: str, semantic_type: str) -> GovernedVersionPin:
        return GovernedVersionPin(
            self._id(f"{namespace}-subject", value),
            self._id(f"{namespace}-version", f"{value}-v1"),
            semantic_type,
            f"{semantic_type}/state",
            "Retained",
        )

    def _manifest(self, document_record: CanonicalRecord):
        workflow = self._pin("workflow", "tender-prebid", "product.tender-prebid-workflow")
        material = GovernedVersionPin.from_record(document_record)
        execution = self._pin("execution", "stage1-run", "platform.execution-context")
        result = self._pin("result", "reviewed-package-ref", "product.client-ready-package-reference")
        event = self._pin("event", "stage1-reconstruction-evidence", "platform.event")
        execution_subject = execution.subject_id
        provenance = tuple(
            dict.fromkeys(
                (
                    self.actor.actual_principal.principal_id,
                    execution_subject,
                    workflow.subject_id,
                    workflow.version_id,
                    material.subject_id,
                    material.version_id,
                    self.contract.record.subject_id,
                    self.contract.record.version_id,
                    execution.subject_id,
                    execution.version_id,
                    result.subject_id,
                    result.version_id,
                    event.subject_id,
                    event.version_id,
                )
            )
        )
        manifest = ReconstructionManifest(
            organization=self.organization,
            execution_subject_id=execution_subject,
            initiating_actor_id=self.actor.actual_principal.principal_id,
            operation_name="product.tender-prebid.synthetic-stage1-review",
            workflow=workflow,
            material_inputs=(material,),
            gate_decisions=(),
            execution_versions=(execution,),
            results=(result,),
            events=(event,),
            event_types=(("platform.product-integration.stage1-observed", "1"),),
            correlation_refs=(execution_subject,),
            causation_refs=(material.version_id,),
            provenance_refs=provenance,
            product_contract=self.contract.version_pin,
        )
        pins = (workflow, material, self.contract.version_pin, execution, result, event)
        constraints = tuple(
            (pin.version_id, "prebid-review", ("read",), "restricted-pilot")
            for pin in pins
        )
        return manifest, constraints

    def test_exact_p6_02_identity_and_only_cap001_cap004_dependencies_are_preserved(self) -> None:
        self.assertEqual(self.contract.lifecycle.value, "Provisional")
        self.assertEqual(self.contract.product_version, PRODUCT_COMPATIBILITY_LINE)
        self.assertEqual(self.contract.record.version_id.value, "p6-02-arvectum-tender-operator-v0.1.0")
        self.assertEqual(PRODUCT_CONTRACT_VERSION, "0.1.0")
        dependency_ids = {item.dependency_id for item in self.contract.dependencies}
        self.assertEqual(dependency_ids, {CAP_001_DOCUMENT_ARTIFACT, CAP_004_AUDIT_RECONSTRUCTION})
        self.assertNotIn(CAP_002_MEMORY_KNOWLEDGE, dependency_ids)
        self.assertNotIn(CAP_003_SEARCH_PROJECTION, dependency_ids)
        self.assertTrue(all(item.provisional for item in self.contract.dependencies))
        self.assertTrue(
            all(
                set(item.side_effect_classes) == {OperationSideEffectClass.READ_ONLY}
                for item in self.contract.operations
            )
        )

    def test_external_reference_document_resolves_without_native_authority_substitution(self) -> None:
        admitted, artifact = self._external_document()
        reliance = self.adapters.capabilities.resolve_document(
            request=self._request(CAP_001_DOCUMENT_ARTIFACT, OP_RESOLVE_DOCUMENT),
            governed_versions=self.governed_versions,
            admitted=admitted,
            artifact_id=artifact.artifact_id,
        )
        self.assertEqual(reliance.document_version_id, admitted.version_id)
        self.assertIs(admitted.canonical_record.authority_mode, AuthorityMode.EXTERNAL_REFERENCE)
        self.assertEqual(
            admitted.canonical_record.external_authority.authoritative_system,
            "synthetic-redacted-eis-source",
        )

    def test_external_authority_mode_requires_explicit_contract(self) -> None:
        with self.assertRaises(ValueError):
            CanonicalRecord(
                subject_id=self._id("document-subject", "invalid-external"),
                version_id=self._id("document-version", "invalid-external-v1"),
                semantic_type="platform.document",
                schema_version="1",
                organization=self.organization,
                authority_mode=AuthorityMode.EXTERNAL_REFERENCE,
                authority_scope=DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
                accountable_owner_id=self.actor.actual_principal.principal_id,
                creation_actor=self.actor,
                created_at=self.created_at,
                provenance_refs=(self.actor.actual_principal.principal_id,),
                integrity_metadata=(("fixture", "invalid-external"),),
            )

    def test_wrong_organization_fails_closed(self) -> None:
        admitted, artifact = self._external_document()
        other = OrganizationScope(Identity("organization", "p6-03-org-b", "platform"))
        actor_b = ActorContext(
            Principal(Identity("principal", "other-operator", "p6-03-org-b")),
            other,
        )
        access_b = AccessRequest(actor_b, "prebid-review", "read", ("restricted-pilot",))
        with self.assertRaises(ProductContractScopeError):
            self.adapters.capabilities.resolve_document(
                request=self._request(
                    CAP_001_DOCUMENT_ARTIFACT,
                    OP_RESOLVE_DOCUMENT,
                    organization=other,
                    product_id=Identity("product", "arvectum-tender-operator", "p6-03-org-b"),
                    access=access_b,
                ),
                governed_versions=self.governed_versions,
                admitted=admitted,
                artifact_id=artifact.artifact_id,
            )

    def test_purpose_right_and_classification_denials_fail_closed(self) -> None:
        admitted, artifact = self._external_document()
        denied = (
            AccessRequest(self.actor, "other-purpose", "read", ("restricted-pilot",)),
            AccessRequest(self.actor, "prebid-review", "export", ("restricted-pilot",)),
            AccessRequest(self.actor, "prebid-review", "read", ("public",)),
        )
        for access in denied:
            with self.subTest(access=access), self.assertRaises(CrossCapabilityEnforcementError):
                self.adapters.capabilities.resolve_document(
                    request=self._request(
                        CAP_001_DOCUMENT_ARTIFACT,
                        OP_RESOLVE_DOCUMENT,
                        access=access,
                    ),
                    governed_versions=self.governed_versions,
                    admitted=admitted,
                    artifact_id=artifact.artifact_id,
                )

    def test_missing_incompatible_and_deprecated_provider_evidence_fail_closed(self) -> None:
        cap001 = self.governed_versions[0]
        with self.assertRaises(UnsupportedDependencyResolutionError):
            compose_integration_adapters(
                contract=self.contract,
                actor=self.actor,
                effective_product_contract=self.contract.version_pin,
                governed_versions=(cap001,),
            )

        incompatible = (
            cap001,
            GovernedDependencyVersionEvidence(
                CAP_004_AUDIT_RECONSTRUCTION,
                "2.0.0",
                DependencySupportDisposition.SUPPORTED,
                "synthetic-incompatible-provider-evidence",
            ),
        )
        with self.assertRaises(IncompatibleDependencyVersionError):
            compose_integration_adapters(
                contract=self.contract,
                actor=self.actor,
                effective_product_contract=self.contract.version_pin,
                governed_versions=incompatible,
            )

        deprecated = (
            cap001,
            GovernedDependencyVersionEvidence(
                CAP_004_AUDIT_RECONSTRUCTION,
                CAPABILITY_CONTRACT_VERSION,
                DependencySupportDisposition.DEPRECATED,
                "synthetic-stale-provider-evidence",
                migration_obligation="review provider mapping before further reliance",
            ),
        )
        with self.assertRaises(DeprecatedDependencyResolutionError):
            compose_integration_adapters(
                contract=self.contract,
                actor=self.actor,
                effective_product_contract=self.contract.version_pin,
                governed_versions=deprecated,
            )

    def test_current_provider_evidence_cannot_be_omitted_after_composition(self) -> None:
        admitted, artifact = self._external_document()
        with self.assertRaises(IntegrationCompositionEvidenceRequiredError):
            self.adapters.capabilities.resolve_document(
                request=self._request(CAP_001_DOCUMENT_ARTIFACT, OP_RESOLVE_DOCUMENT),
                governed_versions=None,
                admitted=admitted,
                artifact_id=artifact.artifact_id,
            )

    def test_incomplete_reconstruction_is_truthful_and_does_not_invent_evidence(self) -> None:
        admitted, _ = self._external_document()
        manifest, constraints = self._manifest(admitted.canonical_record)
        restricted_version = manifest.material_inputs[0].version_id
        constrained = tuple(
            (version_id, purpose, rights, "more-restricted")
            if version_id == restricted_version
            else (version_id, purpose, rights, classification)
            for version_id, purpose, rights, classification in constraints
        )
        view = self.adapters.capabilities.reconstruct_execution(
            request=self._request(CAP_004_AUDIT_RECONSTRUCTION, OP_RECONSTRUCT_EXECUTION),
            governed_versions=self.governed_versions,
            manifest=manifest,
            evidence_constraints=constrained,
        )
        self.assertFalse(view.complete)
        restricted = next(item for item in view.evidence if item.version_id == restricted_version)
        self.assertIs(restricted.availability, EvidenceAvailability.REDACTED)
        self.assertIsNone(restricted.source)

    def test_hidden_private_platform_coupling_mechanisms_are_rejected(self) -> None:
        for mechanism in (
            ProductBoundaryMechanism.INTERNAL_TABLE,
            ProductBoundaryMechanism.INTERNAL_IMPORT,
            ProductBoundaryMechanism.UNDOCUMENTED_ENDPOINT,
            ProductBoundaryMechanism.PRIVATE_EVENT_STREAM,
            ProductBoundaryMechanism.IMPLICIT_SHARED_STATE,
        ):
            with self.subTest(mechanism=mechanism), self.assertRaises(HiddenProductPlatformCouplingError):
                self.adapters.capabilities.admit(
                    self._request(
                        CAP_001_DOCUMENT_ARTIFACT,
                        OP_RESOLVE_DOCUMENT,
                        mechanism=mechanism,
                    ),
                    governed_versions=self.governed_versions,
                )


if __name__ == "__main__":
    unittest.main()
