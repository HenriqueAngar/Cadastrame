"""Tela inicial do módulo de Estoque."""

from __future__ import annotations

from ui.components.modules.assets import AssetRegistry
from ui.components.modules.module import Module, ModuleDefinition


class EstoqueModule:
    def __init__(self) -> None:
        self._module = Module(
            definition=ModuleDefinition(
                key="estoque",
                title="Estoque",
                icon="📦",
                resource_page_code="estoque",
                placeholder="Aqui haverá formulários do módulo de Estoque.",
            ),
            assets=AssetRegistry(),
        )

    def respond(self) -> None:
        self._module.respond()
