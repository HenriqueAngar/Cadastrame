import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from infraesctruture.auth.manager import AuthManager
from infraesctruture.auth.utils.models import Resource, UserContext
from infraesctruture.auth.utils.handler import AccessDeniedError, PasswordAlreadySetError
from services.rh.rh_service import RHService
from services.pcp.pcp_service import BasePrecosService
from services.producao.producao_service import ProducaoService
from shared.records import Records


class AuthorizationTests(unittest.TestCase):
    def setUp(self):
        self.auth = AuthManager.__new__(AuthManager)
        self.auth._provider = Mock()
        self.auth._session = Mock()
        self.auth._session.authenticated = True
        self.auth._session.expired.return_value = False
        self.auth._session.user = UserContext(7, 4, "Teste", "test@example.invalid", ())
        self.record = SimpleNamespace(iduser=7, idrole=4, username="Teste", email="test@example.invalid", active=True, password="existing-hash")
        self.auth._provider.get_user_by_id.return_value = self.record
        self.auth._provider.get_user_by_email.return_value = self.record
        self.auth._provider.get_role_resources.return_value = []
        self.auth._session.update_user.side_effect = lambda user: setattr(self.auth._session, "user", user)

    def test_revoked_permission_is_not_kept_from_session(self):
        self.auth._session.user = UserContext(7, 4, "Teste", "test@example.invalid", (Resource(8, "rh", "extras", "Extras"),))
        with self.assertRaises(AccessDeniedError):
            self.auth.require_resource("rh", "extras")
        self.assertEqual(self.auth._session.user.resources, ())

    def test_role_change_is_loaded_before_authorization(self):
        self.record.idrole = 3
        self.auth._provider.get_role_resources.return_value = [Resource(6, "production", "packing", "Ensaque")]
        self.auth.require_resource("production", "packing")
        self.assertEqual(self.auth._session.user.idrole, 3)
        with self.assertRaises(AccessDeniedError):
            self.auth.require_resource("rh", "extras")

    def test_deactivated_account_loses_session(self):
        self.auth._provider.get_user_by_id.return_value = None
        self.assertFalse(self.auth.refresh())
        self.auth._session.logout.assert_called_once()

    def test_expired_session_is_not_refreshed(self):
        self.auth._session.expired.return_value = True
        with self.assertRaises(AccessDeniedError):
            self.auth.require_resource("rh", "extras")
        self.auth._provider.get_user_by_id.assert_not_called()

    def test_database_failure_closes_session(self):
        self.auth._provider.get_user_by_id.side_effect = RuntimeError("unavailable")
        with self.assertRaises(RuntimeError):
            self.auth.refresh()
        self.auth._session.logout.assert_called_once()

    def test_first_access_cannot_overwrite_existing_password(self):
        with self.assertRaises(PasswordAlreadySetError):
            self.auth.create_password("test@example.invalid", "test-password")
        self.auth._provider.update_password.assert_not_called()
        self.auth._session.login.assert_not_called()

    def test_resource_identity_uses_codes_not_database_id(self):
        self.auth._provider.get_role_resources.return_value = [Resource(999, "rh", "extras", "Extras")]
        self.auth.require_resource("rh", "extras")

    @patch("infraesctruture.auth.authorization.AuthManager")
    def test_all_write_actions_reject_before_domain(self, manager):
        manager.return_value.require_resource.side_effect = AccessDeniedError()
        for service, actions in [
            (RHService(), ["extras"]),
            (BasePrecosService(), ["baseprecos"]),
            (ProducaoService(), ["ensaques", "paradas", "output"]),
        ]:
            domains = {action: Mock() for action in actions}
            service.domain = domains
            for action in actions:
                with self.subTest(action=action):
                    with self.assertRaises(AccessDeniedError):
                        service.process(action, Records())
                    with self.assertRaises(AccessDeniedError):
                        getattr(service, action)(Records())
                    self.assertEqual(domains[action].mock_calls, [])

    @patch("infraesctruture.auth.authorization.AuthManager")
    def test_permitted_write_reaches_domain(self, manager):
        service = RHService()
        domain = Mock()
        records = Records()
        domain.identificar.return_value = records
        domain.registrar.return_value = 1
        service.domain = {"extras": domain}
        self.assertEqual(service.process("extras", records).data["total"], 1)
        manager.return_value.require_resource.assert_called_once_with("rh", "extras")

    def test_unknown_operation_is_rejected(self):
        for service in [RHService(), BasePrecosService(), ProducaoService()]:
            with self.assertRaises(AccessDeniedError):
                service.process("__init__", Records())
