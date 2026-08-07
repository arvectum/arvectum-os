from dataclasses import FrozenInstanceError
import unittest

from arvectum_os_ref import ActorContext, Identity, OrganizationScope, Principal


class IdentityTests(unittest.TestCase):
    def test_identity_requires_explicit_non_empty_namespace_value_and_scope(self) -> None:
        for kwargs in (
            {"namespace": "", "value": "org-1", "scope": "platform"},
            {"namespace": "organization", "value": "", "scope": "platform"},
            {"namespace": "organization", "value": "org-1", "scope": ""},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                Identity(**kwargs)

    def test_identity_is_immutable(self) -> None:
        identity = Identity("principal", "p-1", "platform")
        with self.assertRaises(FrozenInstanceError):
            identity.value = "p-2"  # type: ignore[misc]


class OrganizationAndActorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org_a = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.org_b = OrganizationScope(Identity("organization", "org-b", "platform"))
        self.principal = Principal(Identity("principal", "principal-1", "platform"))

    def test_organization_scope_is_required_and_has_no_default_fallback(self) -> None:
        with self.assertRaises(ValueError):
            OrganizationScope(None)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            ActorContext(self.principal, None)  # type: ignore[arg-type]

    def test_same_principal_can_act_in_different_organization_scopes(self) -> None:
        actor_a = ActorContext(self.principal, self.org_a)
        actor_b = ActorContext(self.principal, self.org_b)

        self.assertEqual(actor_a.actual_principal.principal_id, actor_b.actual_principal.principal_id)
        self.assertNotEqual(actor_a.organization.organization_id, actor_b.organization.organization_id)

    def test_acting_on_behalf_of_preserves_actual_and_represented_principals(self) -> None:
        represented = Principal(Identity("principal", "represented-1", "platform"))
        actor = ActorContext(
            actual_principal=self.principal,
            organization=self.org_a,
            represented_principal=represented,
        )

        self.assertEqual(actor.actual_principal, self.principal)
        self.assertEqual(actor.represented_principal, represented)
        self.assertNotEqual(actor.actual_principal, actor.represented_principal)

    def test_service_or_ai_identity_can_be_attributed_without_encoding_role_in_identity(self) -> None:
        for value in ("service-1", "ai-agent-1"):
            principal = Principal(Identity("principal", value, "platform"))
            actor = ActorContext(principal, self.org_a)
            self.assertEqual(actor.actual_principal.principal_id.value, value)

    def test_authentication_evidence_is_reference_only_not_authority(self) -> None:
        evidence = Identity("authentication-evidence", "authn-1", "org-a")
        actor = ActorContext(
            self.principal,
            self.org_a,
            authentication_evidence_refs=(evidence,),
        )

        self.assertEqual(actor.authentication_evidence_refs, (evidence,))
        self.assertFalse(hasattr(actor, "authorized"))
        self.assertFalse(hasattr(actor, "organizational_authority"))


if __name__ == "__main__":
    unittest.main()
