from dataclasses import replace
import json
import unittest

from arvectum_os_ref.canonical import build_p1_02_native_record
from arvectum_os_ref.events import admit_p1_07_event, build_p1_07_event_candidate
from arvectum_os_ref.execution import start_p1_04_execution
from arvectum_os_ref.gates import (
    GateKind,
    GateOutcome,
    admit_p1_05_ready_execution,
    build_p1_05_gate_decision,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.mutation import execute_p1_06_canonical_mutation
from arvectum_os_ref.observation import build_p1_09_observation
from arvectum_os_ref.portability import (
    PortableFixtureExportError,
    PortableSemanticFixture,
    export_p1_10_semantic_fixture,
)
from arvectum_os_ref.provenance import build_p1_08_reconstruction_evidence
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import build_p1_03_workflow


class P110PortableSemanticFixtureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "principal-1", "platform"))
        self.actor = ActorContext(self.principal, self.organization)
        self.decision_principal = Principal(Identity("principal", "principal-2", "platform"))
        self.decision_actor = ActorContext(self.decision_principal, self.organization)
        self.subject = build_p1_02_native_record(
            organization=self.organization,
            actor=self.actor,
        )
        self.workflow = build_p1_03_workflow(
            organization=self.organization,
            actor=self.actor,
            target_record=self.subject,
        )
        self.awaiting = start_p1_04_execution(
            organization=self.organization,
            actor=self.actor,
            workflow=self.workflow,
            material_input=self.subject,
        )
        self.authorization = build_p1_05_gate_decision(
            execution=self.awaiting,
            kind=GateKind.AUTHORIZATION,
            outcome=GateOutcome.ALLOW,
            decision_actor=self.decision_actor,
            basis_ref=Identity("governed-basis", "authorization-fixture-v1", "org-a"),
        )
        self.organizational_authority = build_p1_05_gate_decision(
            execution=self.awaiting,
            kind=GateKind.ORGANIZATIONAL_AUTHORITY,
            outcome=GateOutcome.ALLOW,
            decision_actor=self.decision_actor,
            basis_ref=Identity("governed-basis", "authority-fixture-v1", "org-a"),
        )
        self.ready = admit_p1_05_ready_execution(
            execution=self.awaiting,
            authorization=self.authorization,
            organizational_authority=self.organizational_authority,
        )
        self.mutation = execute_p1_06_canonical_mutation(
            execution=self.ready,
            workflow=self.workflow,
            authorization=self.authorization,
            organizational_authority=self.organizational_authority,
            current_record=self.subject,
            new_version_id=Identity("canonical-version", "subject-1-v2", "org-a"),
            new_payload=(("label", "domain-neutral reference subject updated"),),
        )
        candidate = build_p1_07_event_candidate(mutation=self.mutation)
        self.event = admit_p1_07_event(
            candidate=candidate,
            mutation=self.mutation,
        ).event
        self.evidence = build_p1_08_reconstruction_evidence(
            input_record=self.subject,
            workflow=self.workflow,
            awaiting_execution=self.awaiting,
            authorization=self.authorization,
            organizational_authority=self.organizational_authority,
            ready_execution=self.ready,
            mutation=self.mutation,
            event=self.event,
        )
        self.observation = build_p1_09_observation(
            evidence=self.evidence,
            event=self.event,
            mutation=self.mutation,
        )

    @staticmethod
    def _identity(identity: Identity) -> dict[str, str]:
        return {
            "namespace": identity.namespace,
            "value": identity.value,
            "scope": identity.scope,
        }

    def _export(self, **overrides) -> PortableSemanticFixture:
        arguments = {
            "input_record": self.subject,
            "workflow": self.workflow,
            "awaiting_execution": self.awaiting,
            "authorization": self.authorization,
            "organizational_authority": self.organizational_authority,
            "ready_execution": self.ready,
            "mutation": self.mutation,
            "event": self.event,
            "evidence": self.evidence,
            "observation": self.observation,
        }
        arguments.update(overrides)
        return export_p1_10_semantic_fixture(**arguments)

    def _document(self, **overrides):
        return json.loads(self._export(**overrides).serialized)

    @staticmethod
    def _record(document, role: str):
        matches = [record for record in document["records"] if record["role"] == role]
        if len(matches) != 1:
            raise AssertionError(f"expected one exported record for role {role}")
        return matches[0]

    def test_exports_documented_json_without_python_object_layout(self) -> None:
        fixture = self._export()
        document = json.loads(fixture.serialized)

        self.assertIsInstance(fixture, PortableSemanticFixture)
        self.assertEqual(document["fixture"]["format_id"], "arvectum-os.phase1.semantic-fixture")
        self.assertEqual(document["fixture"]["format_version"], "1")
        self.assertEqual(document["fixture"]["media_type"], "application/json")
        for python_layout_marker in (
            "arvectum_os_ref",
            "CanonicalRecord(",
            "Identity(",
            "WorkflowDefinition(",
            "__class__",
            "__dict__",
        ):
            self.assertNotIn(python_layout_marker, fixture.serialized)

    def test_fixture_declares_bounded_non_authoritative_non_public_scope(self) -> None:
        document = self._document()
        metadata = document["fixture"]

        self.assertEqual(metadata["scope"], "P1.01-P1.10")
        self.assertEqual(metadata["status"], "bounded-reference-fixture")
        self.assertFalse(metadata["canonical_authority"])
        self.assertTrue(metadata["derived_representation"])
        self.assertFalse(metadata["public_compatibility_contract"])
        self.assertFalse(metadata["production_export_endpoint"])
        self.assertFalse(document["portability"]["export_authorization_mechanism"])

    def test_organization_and_actor_attribution_are_preserved(self) -> None:
        document = self._document()

        self.assertEqual(
            document["organization"]["organization_id"],
            self._identity(self.organization.organization_id),
        )
        actors = {actor["role"]: actor for actor in document["actors"]}
        self.assertEqual(
            actors["initiating-actor"]["actual_principal_id"],
            self._identity(self.principal.principal_id),
        )
        self.assertEqual(
            actors["gate-decision-actor"]["actual_principal_id"],
            self._identity(self.decision_principal.principal_id),
        )
        self.assertEqual(
            actors["initiating-actor"]["organization_id"],
            self._identity(self.organization.organization_id),
        )

    def test_manifest_preserves_each_expected_immutable_record_version_once(self) -> None:
        document = self._document()
        expected_versions = {
            record.version_id
            for record in (
                self.subject,
                self.workflow.record,
                self.authorization.record,
                self.organizational_authority.record,
                self.awaiting.record,
                self.ready.record,
                self.mutation.resulting_record,
                self.mutation.execution.record,
                self.event.record,
                self.observation.record,
            )
        }
        exported_versions = {
            (
                item["namespace"],
                item["value"],
                item["scope"],
            )
            for item in document["manifest"]["record_versions"]
        }
        expected_version_values = {
            (identity.namespace, identity.value, identity.scope)
            for identity in expected_versions
        }

        self.assertEqual(document["manifest"]["record_count"], 10)
        self.assertEqual(len(document["records"]), 10)
        self.assertEqual(exported_versions, expected_version_values)
        self.assertEqual(len(exported_versions), 10)

    def test_canonical_envelopes_preserve_authority_schema_lifecycle_and_predecessors(self) -> None:
        document = self._document()
        input_record = self._record(document, "material-input-v1")["canonical_record"]
        result_record = self._record(document, "canonical-result-v2")["canonical_record"]
        ready_record = self._record(document, "execution-ready")["canonical_record"]
        terminal_record = self._record(document, "execution-succeeded")["canonical_record"]

        self.assertEqual(input_record["authority"]["mode"], "Native")
        self.assertEqual(input_record["authority"]["scope"], "reference.subject/state")
        self.assertEqual(input_record["schema_version"], "1")
        self.assertEqual(result_record["semantic_type"], self.subject.semantic_type)
        self.assertEqual(
            result_record["predecessor_version_identity"],
            self._identity(self.subject.version_id),
        )
        self.assertEqual(
            ready_record["predecessor_version_identity"],
            self._identity(self.awaiting.execution_version_id),
        )
        self.assertEqual(
            terminal_record["predecessor_version_identity"],
            self._identity(self.ready.execution_version_id),
        )

    def test_execution_semantics_preserve_exact_workflow_input_gate_and_effect_pins(self) -> None:
        document = self._document()
        awaiting = self._record(document, "execution-awaiting-gate")["execution"]
        ready = self._record(document, "execution-ready")["execution"]
        terminal = self._record(document, "execution-succeeded")["execution"]

        self.assertEqual(
            awaiting["workflow"]["version_identity"],
            self._identity(self.workflow.workflow_version_id),
        )
        self.assertEqual(
            awaiting["material_inputs"][0]["version_identity"],
            self._identity(self.subject.version_id),
        )
        self.assertEqual(len(awaiting["gate_decisions"]), 0)
        self.assertEqual(
            [pin["version_identity"] for pin in ready["gate_decisions"]],
            [
                self._identity(self.authorization.record.version_id),
                self._identity(self.organizational_authority.record.version_id),
            ],
        )
        self.assertEqual(
            terminal["canonical_effects"][0]["version_identity"],
            self._identity(self.mutation.resulting_record.version_id),
        )

    def test_semantic_links_distinguish_subject_and_version_reference_roles(self) -> None:
        document = self._document()
        correlation = [
            link for link in document["semantic_links"] if link["kind"] == "correlation"
        ]
        causation = [
            link for link in document["semantic_links"] if link["kind"] == "causation"
        ]

        self.assertEqual(len(correlation), 1)
        self.assertEqual(len(causation), 1)
        self.assertEqual(correlation[0]["source"]["reference_role"], "version")
        self.assertEqual(correlation[0]["target"]["reference_role"], "subject")
        self.assertEqual(
            correlation[0]["target"]["identity"],
            self._identity(self.mutation.execution.execution_subject_id),
        )
        self.assertEqual(causation[0]["target"]["reference_role"], "version")
        self.assertEqual(
            causation[0]["target"]["identity"],
            self._identity(self.mutation.execution.execution_version_id),
        )

    def test_event_semantics_and_provenance_are_preserved(self) -> None:
        document = self._document()
        exported = self._record(document, "canonical-event")
        event = exported["event"]
        envelope = exported["canonical_record"]

        self.assertEqual(event["event_type"], self.event.event_type)
        self.assertEqual(event["event_schema_version"], self.event.event_schema_version)
        self.assertEqual(event["authoritative_source"], "Arvectum OS")
        self.assertEqual(
            event["execution_version"]["identity"],
            self._identity(self.mutation.execution.execution_version_id),
        )
        self.assertEqual(
            event["related_versions"][0]["identity"],
            self._identity(self.mutation.resulting_record.version_id),
        )
        provenance = {
            (item["namespace"], item["value"], item["scope"])
            for item in envelope["provenance_refs"]
        }
        self.assertIn(
            (
                self.mutation.execution.execution_version_id.namespace,
                self.mutation.execution.execution_version_id.value,
                self.mutation.execution.execution_version_id.scope,
            ),
            provenance,
        )

    def test_observation_remains_unvalidated_and_not_promoted_to_knowledge(self) -> None:
        document = self._document()
        exported = self._record(document, "observation")
        observation = exported["observation"]
        semantic_types = {
            record["canonical_record"]["semantic_type"] for record in document["records"]
        }

        self.assertEqual(observation["epistemic_status"], "Unvalidated")
        self.assertEqual(observation["knowledge_promotion"], "not-performed")
        self.assertEqual(
            observation["source_event"]["version_identity"],
            self._identity(self.event.record.version_id),
        )
        self.assertEqual(
            observation["source_execution"]["version_identity"],
            self._identity(self.mutation.execution.record.version_id),
        )
        self.assertNotIn("platform.knowledge", semantic_types)

    def test_reconstruction_is_exported_as_derived_non_canonical_evidence(self) -> None:
        document = self._document()
        reconstruction = document["reconstruction"]

        self.assertEqual(reconstruction["authority_status"], "derived-non-canonical")
        self.assertEqual(
            reconstruction["workflow"]["version_identity"],
            self._identity(self.workflow.workflow_version_id),
        )
        self.assertEqual(
            reconstruction["execution_versions"][-1]["version_identity"],
            self._identity(self.mutation.execution.execution_version_id),
        )
        self.assertEqual(
            reconstruction["events"][0]["version_identity"],
            self._identity(self.event.record.version_id),
        )

    def test_exported_links_do_not_fabricate_canonical_typed_relationship_records(self) -> None:
        document = self._document()

        self.assertEqual(document["manifest"]["canonical_typed_relationship_record_count"], 0)
        self.assertTrue(document["semantic_links"])
        self.assertTrue(
            all(not link["canonical_typed_relationship"] for link in document["semantic_links"])
        )
        self.assertTrue(
            all(
                record["canonical_record"]["semantic_type"] != "platform.relationship"
                for record in document["records"]
            )
        )

    def test_portability_manifest_does_not_claim_secret_or_production_export(self) -> None:
        document = self._document()
        portability = document["portability"]

        self.assertEqual(portability["representation"], "documented-json-semantic-fixture")
        self.assertFalse(portability["canonical_authority"])
        self.assertFalse(portability["public_compatibility_contract"])
        self.assertFalse(portability["export_authorization_mechanism"])
        self.assertEqual(portability["non_exportable_dependencies"], [])
        self.assertTrue(portability["explicit_omissions"])

    def test_export_is_deterministic_observational_and_does_not_mutate_sources(self) -> None:
        source_snapshot = (
            self.subject,
            self.workflow,
            self.awaiting,
            self.authorization,
            self.organizational_authority,
            self.ready,
            self.mutation,
            self.event,
            self.evidence,
            self.observation,
        )

        first = self._export()
        second = self._export()

        self.assertEqual(first.serialized, second.serialized)
        self.assertEqual(
            source_snapshot,
            (
                self.subject,
                self.workflow,
                self.awaiting,
                self.authorization,
                self.organizational_authority,
                self.ready,
                self.mutation,
                self.event,
                self.evidence,
                self.observation,
            ),
        )

    def test_parsed_mapping_is_detached_from_immutable_serialized_fixture(self) -> None:
        fixture = self._export()
        parsed = fixture.to_mapping()
        parsed["fixture"]["canonical_authority"] = True

        reparsed = fixture.to_mapping()
        self.assertFalse(reparsed["fixture"]["canonical_authority"])
        self.assertFalse(json.loads(fixture.serialized)["fixture"]["canonical_authority"])

    def test_wrong_reconstruction_evidence_fails_closed(self) -> None:
        forged = replace(self.evidence, operation_name="different-operation")

        with self.assertRaisesRegex(PortableFixtureExportError, "exact P1.08 reconstruction"):
            self._export(evidence=forged)

    def test_wrong_observation_state_fails_closed(self) -> None:
        forged_record = replace(
            self.observation.record,
            payload=(("operation", "forged-operation"),),
        )
        forged = replace(self.observation, record=forged_record)

        with self.assertRaisesRegex(PortableFixtureExportError, "exact P1.09 Observation"):
            self._export(observation=forged)


if __name__ == "__main__":
    unittest.main()
