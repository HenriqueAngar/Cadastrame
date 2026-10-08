"""Tela inicial do módulo de PCP."""

from __future__ import annotations

from ui.components.modules.assets import AssetRegistry
from ui.components.modules.module import Module, ModuleDefinition


class PCPModule:
    def __init__(self) -> None:
        self._module = Module(
            definition=ModuleDefinition(
                key="pcp",
                title="PCP",
                icon="📋",
                resource_page_code="pcp",
                placeholder="Aqui haverá formulários do módulo de PCP.",
            ),
            assets=AssetRegistry(),
        )

    def respond(self) -> None:
        self._module.respond()
