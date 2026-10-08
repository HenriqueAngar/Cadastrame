"""Módulo genérico de Cadastros."""

from __future__ import annotations

from ui.components.modules.assets import AssetRegistry
from ui.components.modules.module import Module, ModuleDefinition


class CadastrosModule:
    """Agrupa assets de manutenção de registros."""

    def __init__(self) -> None:
        self._module = Module(
            definition=ModuleDefinition(
                key="cadastros",
                title="Cadastros",
                icon="🗂️",
                placeholder="Aqui haverão formulários de cadastro. Esta área será desenvolvida em uma próxima etapa.",
            ),
            assets=AssetRegistry(),
        )

    def respond(self) -> None:
        return self._module.respond()
