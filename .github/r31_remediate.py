from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(path: str, old: str, new: str, *, count: int = 1) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    actual = text.count(old)
    if actual != count:
        raise RuntimeError(f"{path}: expected {count} matches, found {actual}: {old[:120]!r}")
    target.write_text(text.replace(old, new, count), encoding="utf-8")


# Backend Copilot contract: source context is not presented as fact, and AI cannot
# jump generically to an unrelated governed execution.
copilot = "reference/python/workspace_app/copilot.py"
replace(copilot, "never promoted to sourced fact or validated Knowledge.", "never promoted to source context, validated Knowledge, or authority.")
replace(copilot, '"schema": "arvectum.workspace.copilot-answer/1"', '"schema": "arvectum.workspace.copilot-answer/2"')
replace(
    copilot,
    '"sourced_fact_distinct_from_synthesis": True,\n                "uncertainty_explicit": True,',
    '"source_context_distinct_from_synthesis": True,\n                "unvalidated_knowledge_not_presented_as_fact": True,\n                "uncertainty_explicit": True,',
)
replace(
    copilot,
    '"follow_up": {\n                "kind": "governed-review",\n                "label": "Review governed actions",\n                "href": "/governed",\n                "direct_consequential_action": False,\n                "routes_to_governed_execution": True,\n            },',
    '"follow_up": {\n                "kind": "inspect-evidence-first",\n                "label": "Inspect cited evidence before action",\n                "href": self.sources[0].open_href if self.sources else None,\n                "direct_consequential_action": False,\n                "routes_to_governed_execution": False,\n                "context_bound_governed_continuation_required": True,\n            },',
)
replace(copilot, 'kind="sourced-fact"', 'kind="source-context"')
replace(copilot, "The sourced evidence above remains inspectable", "The source context above remains inspectable")
replace(copilot, "Only source-grounded facts are shown.", "Only source-grounded context is shown; it is not promoted to validated Knowledge.")

# Frontend presentation and internal TypeScript contract.
types = "reference/python/workspace_frontend/src/types.ts"
replace(types, 'export type CopilotClaimKind = "sourced-fact" | "synthesis" | "uncertainty" | "unavailable-evidence";', 'export type CopilotClaimKind = "source-context" | "synthesis" | "uncertainty" | "unavailable-evidence";')
replace(types, 'schema: "arvectum.workspace.copilot-answer/1";', 'schema: "arvectum.workspace.copilot-answer/2";')
replace(
    types,
    'sourced_fact_distinct_from_synthesis: true;\n    uncertainty_explicit: true;',
    'source_context_distinct_from_synthesis: true;\n    unvalidated_knowledge_not_presented_as_fact: true;\n    uncertainty_explicit: true;',
)
replace(
    types,
    'follow_up: {\n    kind: "governed-review";\n    label: string;\n    href: "/governed";\n    direct_consequential_action: false;\n    routes_to_governed_execution: true;\n  };',
    'follow_up: {\n    kind: "inspect-evidence-first";\n    label: string;\n    href: string | null;\n    direct_consequential_action: false;\n    routes_to_governed_execution: false;\n    context_bound_governed_continuation_required: true;\n  };',
)

ui = "reference/python/workspace_frontend/src/Copilot.tsx"
replace(ui, '"sourced-fact": "Sourced fact",', '"source-context": "Source context",')
replace(ui, "Arvectum separates sourced facts, AI synthesis, uncertainty and unavailable", "Arvectum separates source context, AI synthesis, uncertainty and unavailable")
replace(ui, "Free-form model output can only appear as synthesis, never as sourced fact.", "Free-form model output can only appear as synthesis, never as source context or validated Knowledge.")
replace(
    ui,
    '<p>Review the current governed execution/decision gates. Copilot does not execute the consequence itself.</p>\n            </div>\n            <a className="quiet-link" href={answer.follow_up.href}>{answer.follow_up.label}</a>',
    '<p>Inspect the cited evidence or product context first. A governed continuation may be offered only from context actually bound to the relevant execution or decision. Copilot does not choose an unrelated execution.</p>\n            </div>\n            {answer.follow_up.href ? <a className="quiet-link" href={answer.follow_up.href}>{answer.follow_up.label}</a> : <span className="boundary-note">No context-bound continuation is available.</span>}',
)

# Backend regression evidence.
test = "reference/python/workspace_tests/test_copilot.py"
replace(test, 'self.assertIn("sourced-fact", kinds)', 'self.assertIn("source-context", kinds)')
replace(test, 'self.assertTrue(payload["follow_up"]["routes_to_governed_execution"])', 'self.assertFalse(payload["follow_up"]["routes_to_governed_execution"])\n        self.assertEqual(payload["follow_up"]["kind"], "inspect-evidence-first")\n        self.assertEqual(payload["follow_up"]["href"], "/objects/" + "a" * 20)\n        self.assertTrue(payload["follow_up"]["context_bound_governed_continuation_required"])')
replace(test, 'self.assertTrue(any(claim["kind"] == "sourced-fact" for claim in payload["claims"]))', 'self.assertTrue(any(claim["kind"] == "source-context" for claim in payload["claims"]))')
replace(test, 'claims=(CopilotClaim("sourced-fact", "Inspectable governed evidence.", (source.source_id,)),),', 'claims=(CopilotClaim("source-context", "Inspectable governed evidence.", (source.source_id,)),),')
replace(
    test,
    '    def test_model_outage_never_replaces_missing_synthesis_with_invented_certainty(self) -> None:\n',
    '''    def test_unvalidated_knowledge_role_is_source_context_not_fact(self) -> None:\n        observation = DiscoveryResult(\n            object_id="b" * 20,\n            kind=DiscoveryKind.KNOWLEDGE,\n            semantic_role="Observation",\n            title="Supplier observation",\n            summary="Observation — not validated Knowledge. Governed observation context is available.",\n            source_label="Arvectum OS governed state",\n            authority_mode="Native",\n            state_label="retained · unvalidated",\n            knowledge_role="Observation — not validated Knowledge",\n        )\n        payload = RuntimeCopilotProvider(FakeDiscovery((observation,)), FakeProducts(())).answer(\n            ACCESS, "Что известно про supplier observation?"\n        ).to_payload()\n        source_claims = [claim for claim in payload["claims"] if claim["kind"] == "source-context"]\n        self.assertTrue(source_claims)\n        self.assertTrue(all(claim["kind"] != "sourced-fact" for claim in payload["claims"]))\n        self.assertEqual(payload["sources"][0]["knowledge_role"], "Observation — not validated Knowledge")\n        self.assertTrue(payload["semantics"]["unvalidated_knowledge_not_presented_as_fact"])\n\n    def test_model_outage_never_replaces_missing_synthesis_with_invented_certainty(self) -> None:\n''',
)

# Frontend regression evidence.
front_test = "reference/python/workspace_frontend/src/P908.test.tsx"
replace(front_test, 'release: { id: "p9.08.1", app_api_contract: "6", classification: "bounded-internal-provisional", public_api: false }', 'release: { id: "p9.10.2", app_api_contract: "9", classification: "bounded-internal-provisional", public_api: false }')
replace(front_test, 'schema: "arvectum.workspace.copilot-answer/1"', 'schema: "arvectum.workspace.copilot-answer/2"')
replace(front_test, 'kind: "sourced-fact"', 'kind: "source-context"')
replace(
    front_test,
    'sourced_fact_distinct_from_synthesis: true,\n    uncertainty_explicit: true,',
    'source_context_distinct_from_synthesis: true,\n    unvalidated_knowledge_not_presented_as_fact: true,\n    uncertainty_explicit: true,',
)
replace(
    front_test,
    'kind: "governed-review",\n    label: "Review governed actions",\n    href: "/governed",\n    direct_consequential_action: false,\n    routes_to_governed_execution: true,',
    'kind: "inspect-evidence-first",\n    label: "Inspect cited evidence before action",\n    href: "/objects/aaaaaaaaaaaaaaaaaaaa",\n    direct_consequential_action: false,\n    routes_to_governed_execution: false,\n    context_bound_governed_continuation_required: true,',
)
replace(front_test, 'it("asks naturally, separates claim roles, opens evidence, and routes consequences to governed review"', 'it("asks naturally, separates claim roles, opens evidence, and requires evidence-bound continuation"')
replace(front_test, 'expect(await screen.findByText("Sourced fact")).toBeTruthy();', 'expect(await screen.findByText("Source context")).toBeTruthy();')
replace(front_test, 'expect(screen.getByRole("link", { name: "Review governed actions" }).getAttribute("href")).toBe("/governed");', 'expect(screen.getByRole("link", { name: "Inspect cited evidence before action" }).getAttribute("href")).toBe("/objects/aaaaaaaaaaaaaaaaaaaa");\n    expect(screen.queryByRole("link", { name: "Review governed actions" })).toBeNull();')

# Exact internal application release/contract bump for the changed response shape.
release = ROOT / "reference/python/workspace_app/release.json"
release.write_text('''{\n  "schema": "arvectum.workspace.application-release/1",\n  "release_id": "p9.10.2",\n  "app_api_contract": "9",\n  "classification": "bounded-internal-provisional",\n  "public_api": false\n}\n''', encoding="utf-8")

print("R31 remediation applied")
