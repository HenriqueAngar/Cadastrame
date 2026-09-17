"""Módulo genérico de Cadastros."""

from __future__ import annotations

from ui.components.modules.assets import AssetDefinition, AssetRegistry
from ui.components.modules.module import Module, ModuleDefinition


class CadastrosModule:
    """Agrupa assets de manutenção de registros."""

    def __init__(self) -> None:
        self._module = Module(
            definition=ModuleDefinition(
                key="cadastros",
                title="Cadastros",
                icon="🗂️",
            ),
            assets=AssetRegistry(
                AssetDefinition("cadastro_1", "Cadastro 1", order=1),
                AssetDefinition("cadastro_2", "Cadastro 2", order=2),
            ),
        )

    def respond(self) -> None:
        return self._module.respond()

