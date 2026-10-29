"""Fluxo de identificação do usuário."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Login:
    """
    Estado do fluxo de autenticação.

    O serviço interpreta a autenticação
    e atualiza este objeto para que a UI
    saiba quais formulários exibir.
    """

    email: str = ""

    identified: bool = False

    password_required: bool = False

    first_access: bool = False

    authenticated: bool = False

    error: str | None = None

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def require_password(
        self,
    ) -> None:

        self._clear()

        self.identified = True

        self.password_required = True

    def require_creation(
        self,
    ) -> None:

        self._clear()

        self.identified = True

        self.first_access = True

    def authenticated_success(
        self,
    ) -> None:

        self._clear()

        self.identified = True

        self.authenticated = True

    def fail(
        self,
        message: str,
    ) -> None:

        self._clear()

        self.error = message

    def clear(
        self,
    ) -> None:

        self.email = ""

        self._clear()

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _clear(
        self,
    ) -> None:

        self.identified = False

        self.password_required = False

        self.first_access = False

        self.authenticated = False

        self.error = None