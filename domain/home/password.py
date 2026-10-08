"""Validação das senhas de acesso."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Password:
    value: str
    confirmation: str = ""

    @property
    def empty(self) -> bool:
        return not self.value.strip()

    @property
    def confirmed(self) -> bool:
        return self.value == self.confirmation

    def validate(self, *, require_confirmation: bool = False) -> str | None:
        if self.empty:
            return "Informe uma senha."
        if require_confirmation and not self.confirmed:
            return "As senhas não coincidem."
        return None
