"""Registro dos módulos genéricos da aplicação."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Type

from ui.components.modules.module import ModuleDefinition
from ui.modules.cadastros.cadastros_module import CadastrosModule
from ui.modules.home.home_module import HomeModule
from ui.modules.operacoes.operacoes_module import OperacoesModule


@dataclass(frozen=True, slots=True)
class ModuleRegistration:
    """Metadados e fábrica de um módulo da aplicação."""

    definition: ModuleDefinition
    module: Type

    @property
    def label(self) -> str:
        return f"{self.definition.icon} {self.definition.title}"


MODULES = (
    ModuleRegistration(
        definition=ModuleDefinition(
            key="home",
            title="Home",
            icon="🏠",
            navigator=False,
        ),
        module=HomeModule,
    ),
    ModuleRegistration(
        definition=ModuleDefinition(
            key="cadastros",
            title="Cadastros",
            icon="🗂️",
        ),
        module=CadastrosModule,
    ),
    ModuleRegistration(
        definition=ModuleDefinition(
            key="operacoes",
            title="Operações",
            icon="⚙️",
        ),
        module=OperacoesModule,
    ),
)


class ModuleRegistry:
    """Resolve módulos por chave e preserva a ordem da navegação."""

    def all(self) -> tuple[ModuleRegistration, ...]:
        return MODULES

    def by_key(self, key: str) -> ModuleRegistration:
        for registration in self.all():
            if registration.definition.key == key:
                return registration

        raise ValueError(f"Módulo '{key}' não encontrado.")

    def index(self, key: str) -> int:
        for index, registration in enumerate(self.all()):
            if registration.definition.key == key:
                return index

        return 0

