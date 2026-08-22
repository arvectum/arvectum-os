from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise RuntimeError(f"unexpected match count for {path}: {old[:80]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")

# Preserve RFC-0007 distinctions as a first-class organization-composition field.
replace_once(
    "reference/python/workspace_app/organization.py",
    "    provenance_available: bool\n    canonical_project_record: bool = False\n",
    "    provenance_available: bool\n    semantic_note: str | None = None\n    canonical_project_record: bool = False\n",
)
replace_once(
    "reference/python/workspace_app/organization.py",
    "        if not isinstance(self.provenance_available, bool) or not isinstance(self.canonical_project_record, bool):\n            raise OrganizationCompositionError(\"organization navigation truth flags must be explicit\")\n",
    "        if self.semantic_note is not None:\n            _bounded(self.semantic_note, field=\"semantic_note\", limit=1024)\n        if not isinstance(self.provenance_available, bool) or not isinstance(self.canonical_project_record, bool):\n            raise OrganizationCompositionError(\"organization navigation truth flags must be explicit\")\n",
)
replace_once(
    "reference/python/workspace_app/organization.py",
    "            \"provenance_available\": self.provenance_available,\n            \"canonical_project_record\": self.canonical_project_record,\n",
    "            \"provenance_available\": self.provenance_available,\n            \"semantic_note\": self.semantic_note,\n            \"canonical_project_record\": self.canonical_project_record,\n",
)
replace_once(
    "reference/python/workspace_app/organization.py",
    "                provenance_available=True,\n            )\n            for item in projection.results[:12]\n",
    "                provenance_available=True,\n                semantic_note=item.knowledge_role or item.semantic_role,\n            )\n            for item in projection.results[:12]\n",
)

# Structural composition failures become minimized service-unavailable responses.
replace_once(
    "reference/python/workspace_app/main.py",
    "from .organization import OrganizationCompositionProvider, RuntimeOrganizationCompositionProvider\n",
    "from .organization import OrganizationCompositionError, OrganizationCompositionProvider, RuntimeOrganizationCompositionProvider\n",
)
replace_once(
    "reference/python/workspace_app/main.py",
    '''        _, access = current
        return organization.project(access).to_payload()

    @app.post("/api/app/v1/copilot/ask")
''',
    '''        _, access = current
        try:
            return organization.project(access).to_payload()
        except OrganizationCompositionError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="ORGANIZATION_COMPOSITION_UNAVAILABLE") from None

    @app.post("/api/app/v1/copilot/ask")
''',
)

# Frontend contract + explicit semantics display.
replace_once(
    "reference/python/workspace_frontend/src/types.ts",
    "  provenance_available: boolean;\n  canonical_project_record: false;\n",
    "  provenance_available: boolean;\n  semantic_note: string | null;\n  canonical_project_record: false;\n",
)
replace_once(
    "reference/python/workspace_frontend/src/Organization.tsx",
    '''                <div><dt>Ownership</dt><dd>{item.ownership}</dd></div>
              </dl>
''',
    '''                <div><dt>Ownership</dt><dd>{item.ownership}</dd></div>
                {item.semantic_note ? <div><dt>Semantics</dt><dd>{item.semantic_note}</dd></div> : null}
              </dl>
''',
)

# Test fixtures and assertions.
p = ROOT / "reference/python/workspace_frontend/src/P910.test.tsx"
text = p.read_text(encoding="utf-8")
text = text.replace("provenance_available: true, canonical_project_record", "provenance_available: true, semantic_note: null, canonical_project_record")
p.write_text(text, encoding="utf-8")

replace_once(
    "reference/python/workspace_tests/test_organization_composition.py",
    "                state_label=\"validated\",\n",
    "                state_label=\"validated\",\n                knowledge_role=\"Knowledge Candidate — not validated Knowledge\",\n                semantic_role=\"Knowledge Candidate\",\n",
)
replace_once(
    "reference/python/workspace_tests/test_organization_composition.py",
    "        self.assertEqual(lanes[\"knowledge\"][\"items\"][0][\"href\"], \"/objects/\" + \"a\" * 20)\n",
    "        self.assertEqual(lanes[\"knowledge\"][\"items\"][0][\"href\"], \"/objects/\" + \"a\" * 20)\n        self.assertEqual(lanes[\"knowledge\"][\"items\"][0][\"semantic_note\"], \"Knowledge Candidate — not validated Knowledge\")\n",
)

print("P9.10 review iteration 1 remediation applied")
