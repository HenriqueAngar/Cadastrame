"""Módulo genérico de Operações."""

from __future__ import annotations

from ui.components.modules.assets import AssetDefinition, AssetRegistry
from ui.components.modules.module import Module, ModuleDefinition


class OperacoesModule:
    """Agrupa assets de execução operacional."""

    def __init__(self) -> None:
        self._module = Module(
            definition=ModuleDefinition(
                key="operacoes",
                title="Operações",
                icon="⚙️",
            ),
            assets=AssetRegistry(
                AssetDefinition("operacao_1", "Operação 1", order=1),
                AssetDefinition("operacao_2", "Operação 2", order=2),
                AssetDefinition("operacao_3", "Operação 3", order=3),
            ),
        )

    def respond(self) -> None:
        return self._module.respond()

