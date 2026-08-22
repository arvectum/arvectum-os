from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from arvectum_os_ref.identity import Identity
from workspace_app.access import AccessContext
from workspace_app.config import WorkspaceSettings
from workspace_app.dogfooding import DogfoodingInputError, DogfoodingStore
from workspace_app.main import CSRF_HEADER, RELEASE_HEADER, create_app
from workspace_app.release import load_release


class FakeResolver:
    def __init__(self, organization: str = "org-a", actor: str = "actor-a") -> None:
        self.organization = Identity("organization", organization, "platform")
        self.actor = Identity("principal", actor, organization)

    def authorize(self) -> AccessContext:
        return AccessContext(
            organization=self.organization,
            actor=self.actor,
            principal_kind="human",
            credential_id="credential-test",
            grant_id="grant-test",
        )


def settings(root: Path) -> WorkspaceSettings:
    return WorkspaceSettings(
        runtime_root=root,
        public_origin="http://127.0.0.1:8769",
        bind_host="127.0.0.1",
        bind_port=8769,
        allowed_hosts=("127.0.0.1:8769",),
        organization_label="ООО «Арвектум»",
        actor_label="Owner operator",
        session_idle_seconds=60,
        session_absolute_seconds=300,
        allow_loopback_http=True,
    )


def observation(summary: str = "Repeated navigation friction") -> dict[str, str]:
    return {
        "journey": "J1",
        "surface": "my-work",
        "severity": "material",
        "classification": "workspace-usability",
        "summary": summary,
        "details": "The ordinary path requires an avoidable extra navigation step.",
    }


class DogfoodingStoreTests(unittest.TestCase):
    def test_store_is_non_authoritative_bounded_and_organization_scoped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = DogfoodingStore(root)
            access_a = FakeResolver("org-a", "actor-a").authorize()
            access_b = FakeResolver("org-b", "actor-b").authorize()

            recorded = store.record(access_a, "p9.11-test", observation())
            self.assertEqual(recorded["status"], "open")
            self.assertNotIn("organization_scope_key", recorded)
            self.assertEqual(store.project(access_b).to_payload()["summary"]["total"], 0)

            projection = store.project(access_a).to_payload()
            self.assertEqual(projection["schema"], "arvectum.workspace.dogfooding-backlog/1")
            self.assertFalse(projection["projection"]["canonical_authority"])
            self.assertFalse(projection["projection"]["canonical_event"])
            self.assertFalse(projection["projection"]["validated_knowledge"])
            self.assertFalse(projection["projection"]["organizational_authority_provided"])
            self.assertEqual(projection["summary"]["material_open"], 1)
            self.assertEqual(projection["retention"]["days"], 90)
            self.assertEqual(projection["retention"]["max_items"], 200)

    def test_disposition_preserves_observation_and_requires_rationale(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = DogfoodingStore(Path(tmp))
            access = FakeResolver().authorize()
            recorded = store.record(access, "p9.11-test", observation("Search label is unclear"))
            dispositioned = store.disposition(
                access,
                recorded["id"],
                {"disposition": "resolved", "rationale": "Label changed and the journey was rechecked."},
            )
            self.assertEqual(dispositioned["summary"], "Search label is unclear")
            self.assertEqual(dispositioned["status"], "dispositioned")
            self.assertEqual(dispositioned["disposition"], "resolved")
            projection = store.project(access).to_payload()
            self.assertEqual(projection["summary"]["open"], 0)
            self.assertEqual(projection["summary"]["material_open"], 0)
            with self.assertRaises(DogfoodingInputError):
                store.disposition(access, recorded["id"], {"disposition": "resolved", "rationale": "again"})

    def test_input_taxonomy_is_closed_and_free_text_is_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = DogfoodingStore(Path(tmp))
            access = FakeResolver().authorize()
            invalid = observation()
            invalid["classification"] = "validated-knowledge"
            with self.assertRaises(DogfoodingInputError):
                store.record(access, "p9.11-test", invalid)
            too_long = observation("x" * 241)
            with self.assertRaises(DogfoodingInputError):
                store.record(access, "p9.11-test", too_long)


class DogfoodingBffTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.resolver = FakeResolver()
        self.static = self.root / "dist"
        self.static.mkdir()
        (self.static / "index.html").write_text("<!doctype html><div id='root'></div>", encoding="utf-8")
        self.app = create_app(settings(self.root), access_resolver=self.resolver, static_dir=self.static)
        self.client = TestClient(self.app, base_url="http://127.0.0.1:8769", client=("127.0.0.1", 50000))
        self.release = load_release().release_id
        self.headers = {RELEASE_HEADER: self.release}
        bootstrap = self.client.post(
            "/api/app/v1/session/bootstrap",
            headers={**self.headers, "Origin": "http://127.0.0.1:8769"},
        )
        self.assertEqual(bootstrap.status_code, 200)
        self.csrf = bootstrap.json()["session"]["csrf_token"]

    def tearDown(self) -> None:
        self.client.close()
        self.temp.cleanup()

    def test_capture_and_disposition_require_csrf_and_current_access(self) -> None:
        missing = self.client.post(
            "/api/app/v1/dogfooding/observations",
            headers={**self.headers, "Origin": "http://127.0.0.1:8769"},
            json=observation(),
        )
        self.assertEqual(missing.status_code, 403)

        recorded = self.client.post(
            "/api/app/v1/dogfooding/observations",
            headers={**self.headers, "Origin": "http://127.0.0.1:8769", CSRF_HEADER: self.csrf},
            json=observation(),
        )
        self.assertEqual(recorded.status_code, 200)
        observation_id = recorded.json()["id"]
        backlog = self.client.get("/api/app/v1/dogfooding", headers=self.headers)
        self.assertEqual(backlog.status_code, 200)
        self.assertEqual(backlog.json()["summary"]["material_open"], 1)

        dispositioned = self.client.post(
            f"/api/app/v1/dogfooding/observations/{observation_id}/disposition",
            headers={**self.headers, "Origin": "http://127.0.0.1:8769", CSRF_HEADER: self.csrf},
            json={"disposition": "resolved", "rationale": "Repaired and rechecked in the ordinary path."},
        )
        self.assertEqual(dispositioned.status_code, 200)
        self.assertEqual(self.client.get("/api/app/v1/dogfooding", headers=self.headers).json()["summary"]["open"], 0)

    def test_browser_cannot_select_scope_and_payload_is_minimized(self) -> None:
        recorded = self.client.post(
            "/api/app/v1/dogfooding/observations?organization=evil-org&actor=evil-actor",
            headers={
                **self.headers,
                "Origin": "http://127.0.0.1:8769",
                CSRF_HEADER: self.csrf,
                "X-Organization": "evil-org",
                "X-Actor": "evil-actor",
            },
            json=observation(),
        )
        self.assertEqual(recorded.status_code, 200)
        body = recorded.text
        self.assertNotIn("org-a", body)
        self.assertNotIn("actor-a", body)
        self.assertNotIn("evil-org", body)
        self.assertNotIn("evil-actor", body)


if __name__ == "__main__":
    unittest.main()
