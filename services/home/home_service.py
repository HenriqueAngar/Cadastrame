"""Coordena a identificação, autenticação e criação inicial de senha."""

from __future__ import annotations

from infraesctruture.auth.manager import AuthManager
from infraesctruture.auth.utils.handler import AuthenticationStatus
from domain.home.login import Login
from domain.home.password import Password


class HomeService:
    def __init__(self, auth: AuthManager | None = None) -> None:
        self._auth = auth or AuthManager()

    @property
    def session(self):
        return self._auth.session

    def identify(self, email: str) -> AuthenticationStatus:
        login = Login(email)
        if not login.valid:
            raise ValueError("Informe um e-mail válido.")
        return self._auth.identify(login.normalized_email)

    def authenticate(self, email: str, value: str) -> AuthenticationStatus:
        login = Login(email)
        if not login.valid:
            raise ValueError("Informe um e-mail válido.")

        password = Password(value)
        error = password.validate()
        if error:
            raise ValueError(error)

        return self._auth.login(login.normalized_email, password.value)

    def create_password(
        self,
        email: str,
        value: str,
        confirmation: str,
    ) -> AuthenticationStatus:
        login = Login(email)
        if not login.valid:
            raise ValueError("Informe um e-mail válido.")

        password = Password(value, confirmation)
        error = password.validate(require_confirmation=True)
        if error:
            raise ValueError(error)

        return self._auth.create_password(login.normalized_email, password.value)
