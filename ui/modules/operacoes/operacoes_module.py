"""Módulo genérico de Operações."""

from __future__ import annotations

from ui.components.modules.assets import AssetRegistry
from ui.components.modules.module import Module, ModuleDefinition


class OperacoesModule:
    """Agrupa assets de execução operacional."""

    def __init__(self) -> None:
        self._module = Module(
            definition=ModuleDefinition(
                key="operacoes",
                title="Operações",
                icon="⚙️",
                placeholder="Aqui haverão formulários de operações. Esta área será desenvolvida em uma próxima etapa.",
            ),
            assets=AssetRegistry(),
        )

    def respond(self) -> None:
        return self._module.respond()
