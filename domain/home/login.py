"""Estado e validação da identificação do usuário."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Login:
    email: str

    @property
    def normalized_email(self) -> str:
        return self.email.strip().lower()

    @property
    def valid(self) -> bool:
        email = self.normalized_email
        return bool(email) and "@" in email and " " not in email
