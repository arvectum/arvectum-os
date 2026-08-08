from dataclasses import replace
import inspect
import json
import unittest

import arvectum_os_ref.reference_scenario as reference_scenario_module
from arvectum_os_ref.execution import ExecutionLifecycle, GovernedVersionPin
from arvectum_os_ref.gates import GateKind, GateOutcome
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.observation import ObservationEpistemicStatus
from arvectum_os_ref.reference_scenario import build_p1_reference_scenario
from arvectum_os_ref.runtime import (
    RuntimeComposition,
    default_runtime_operations,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal


class P201RuntimeCompositionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scenario = build_p1_reference_scenario()
        self.result = self.scenario.runtime_result

    def test_reference_scenario_delegates_execution_once_to_runtime_boundary(self) -> None:
        class TrackingRuntime:
            def __init__(self) -> None:
                self.requests = []
                self.delegate = RuntimeComposition()

            def execute(self, request):
                self.requests.append(request)
                return self.delegate.execute(request)

        runtime = TrackingRuntime()
        scenario = build_p1_reference_scenario(runtime=runtime)

        self.assertEqual(len(runtime.requests), 1)
        self.assertIs(runtime.requests[0], scenario.request)
        self.assertEqual(
            scenario.runtime_result.mutation.resulting_record.version_id,
            scenario.request.new_version_id,
        )

    def test_reference_fixture_does_not_import_runtime_orchestration_internals(self) -> None:
        source = inspect.getsource(reference_scenario_module)

        for forbidden_import in (
            "from .execution import",
            "from .gates import",
            "from .mutation import",
            "from .events import",
            "from .provenance import",
            "from .observation import",
        ):
            self.assertNotIn(forbidden_import, source)
        self.assertIn("from .runtime import", source)

    def test_runtime_preserves_execution_lineage_and_exact_version_pins(self) -> None:
        awaiting = self.result.awaiting_execution
        ready = self.result.ready_execution
        terminal = self.result.mutation.execution

        self.assertEqual(awaiting.record.lifecycle_status, ExecutionLifecycle.AWAITING_GATE.value)
        self.assertEqual(ready.record.lifecycle_status, ExecutionLifecycle.READY.value)
        self.assertEqual(terminal.record.lifecycle_status, ExecutionLifecycle.SUCCEEDED.value)
        self.assertEqual(
            awaiting.execution_subject_id,
            ready.execution_subject_id,
        )
        self.assertEqual(ready.execution_subject_id, terminal.execution_subject_id)
        self.assertEqual(
            ready.record.predecessor_version_id,
            awaiting.execution_version_id,
        )
        self.assertEqual(
            terminal.record.predecessor_version_id,
            ready.execution_version_id,
        )
        self.assertEqual(
            awaiting.workflow,
            GovernedVersionPin.from_record(self.scenario.workflow.record),
        )
        self.assertEqual(
            awaiting.material_inputs,
            (GovernedVersionPin.from_record(self.scenario.input_record),),
        )

    def test_runtime_preserves_separate_authorization_and_authority_evidence(self) -> None:
        authorization = self.result.authorization
        organizational_authority = self.result.organizational_authority

        self.assertIs(authorization.kind, GateKind.AUTHORIZATION)
        self.assertIs(organizational_authority.kind, GateKind.ORGANIZATIONAL_AUTHORITY)
        self.assertIs(authorization.outcome, GateOutcome.ALLOW)
        self.assertIs(organizational_authority.outcome, GateOutcome.ALLOW)
        self.assertNotEqual(authorization.record.subject_id, organizational_authority.record.subject_id)
        self.assertEqual(
            self.result.ready_execution.gate_decisions,
            (authorization.version_pin, organizational_authority.version_pin),
        )

    def test_runtime_preserves_mutation_event_and_reconstruction_linkage(self) -> None:
        mutation = self.result.mutation
        event = self.result.event
        evidence = self.result.reconstruction

        self.assertEqual(
            mutation.resulting_record.predecessor_version_id,
            self.scenario.input_record.version_id,
        )
        self.assertEqual(
            mutation.execution.canonical_effects,
            (GovernedVersionPin.from_record(mutation.resulting_record),),
        )
        self.assertEqual(event.execution_subject_id, mutation.execution.execution_subject_id)
        self.assertEqual(event.execution_version_id, mutation.execution.execution_version_id)
        self.assertEqual(event.related_version_ids, (mutation.resulting_record.version_id,))
        self.assertEqual(event.correlation_refs, (mutation.execution.execution_subject_id,))
        self.assertEqual(event.causation_refs, (mutation.execution.execution_version_id,))
        self.assertEqual(
            evidence.execution_versions[-1],
            GovernedVersionPin.from_record(mutation.execution.record),
        )
        self.assertEqual(evidence.events, (GovernedVersionPin.from_record(event.record),))

    def test_runtime_observation_remains_unvalidated_not_knowledge(self) -> None:
        observation = self.result.observation

        self.assertIs(
            observation.epistemic_status,
            ObservationEpistemicStatus.UNVALIDATED,
        )
        self.assertIn(
            ("knowledge-promotion", "not-performed"),
            observation.record.integrity_metadata,
        )
        self.assertEqual(
            observation.source_event,
            GovernedVersionPin.from_record(self.result.event.record),
        )
        self.assertEqual(
            observation.source_execution,
            GovernedVersionPin.from_record(self.result.mutation.execution.record),
        )

    def test_existing_portable_fixture_accepts_runtime_result_without_semantic_drift(self) -> None:
        fixture = self.scenario.export_portable_fixture()
        document = json.loads(fixture.serialized)

        self.assertEqual(document["fixture"]["format_id"], "arvectum-os.phase1.semantic-fixture")
        self.assertEqual(document["fixture"]["scope"], "P1.01-P1.10")
        self.assertFalse(document["fixture"]["canonical_authority"])
        self.assertFalse(document["fixture"]["public_compatibility_contract"])
        self.assertEqual(
            document["reconstruction"]["execution_versions"][-1]["version_identity"]["value"],
            self.result.mutation.execution.execution_version_id.value,
        )

    def test_runtime_operations_are_replaceable_without_changing_fixture_setup(self) -> None:
        calls = []
        defaults = default_runtime_operations()

        def tracking_start_execution(**kwargs):
            calls.append((kwargs["workflow"].workflow_version_id, kwargs["material_input"].version_id))
            return defaults.start_execution(**kwargs)

        runtime = RuntimeComposition(
            operations=replace(defaults, start_execution=tracking_start_execution)
        )
        scenario = build_p1_reference_scenario(runtime=runtime)

        self.assertEqual(
            calls,
            [(scenario.workflow.workflow_version_id, scenario.input_record.version_id)],
        )
        self.assertEqual(
            scenario.runtime_result.mutation.resulting_record.version_id,
            scenario.request.new_version_id,
        )

    def test_required_gate_denial_fails_closed_at_runtime_boundary(self) -> None:
        denied = replace(
            self.scenario.request,
            authorization_outcome=GateOutcome.DENY,
        )

        with self.assertRaises(PermissionError):
            RuntimeComposition().execute(denied)

    def test_cross_organization_decision_actor_is_rejected_before_execution(self) -> None:
        other_organization = OrganizationScope(
            Identity("organization", "org-b", "platform")
        )
        other_actor = ActorContext(
            Principal(Identity("principal", "principal-3", "platform")),
            other_organization,
        )

        with self.assertRaises(ValueError):
            replace(self.scenario.request, decision_actor=other_actor)


if __name__ == "__main__":
    unittest.main()
