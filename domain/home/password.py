"""Fluxo de autenticação por senha."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Password:
    """
    Estado do fluxo de autenticação
    por senha.
    """

    email: str

    value: str = ""

    confirmation: str = ""

    authenticated: bool = False

    created: bool = False

    error: str | None = None

    # ==========================================================
    # VALIDATION
    # ==========================================================

    @property
    def empty(self) -> bool:

        return not self.value.strip()

    @property
    def confirmed(self) -> bool:

        return (
            not self.confirmation
            or self.value == self.confirmation
        )

    @property
    def valid(self) -> bool:

        self.error = None

        if self.empty:

            self.fail(
                "Informe uma senha.",
            )

            return False

        if not self.confirmed:

            self.fail(
                "As senhas não coincidem.",
            )

            return False

        return True

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def authenticated_success(
        self,
    ) -> None:

        self.error = None

        self.created = False

        self.authenticated = True

    def created_success(
        self,
    ) -> None:

        self.error = None

        self.created = True

        self.authenticated = True

    def fail(
        self,
        message: str,
    ) -> None:

        self.error = message

        self.authenticated = False

        self.created = False

    def clear(
        self,
    ) -> None:

        self.value = ""

        self.confirmation = ""

        self.authenticated = False

        self.created = False

        self.error = None