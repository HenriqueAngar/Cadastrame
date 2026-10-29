"""Módulo RH."""

from __future__ import annotations

from shared.records import Records
from services.rh.rh_service import RHService
from ui.components.modules.assets import AssetRegistry
from ui.components.modules.module import Module, ModuleDefinition
from ui.modules.rh.assets.extras import ExtrasAsset


class RHModule:

    def __init__(self):

        self.module = Module(

            definition=ModuleDefinition(
                key="rh",
                title="👥 Recursos Humanos",
            ),

            service=RHService(),

            assets=AssetRegistry(
                ExtrasAsset(order=1),
            ),

        )

    def respond(
        self,
        context: Records | None = None,
        records: Records | None = None,
        **kwargs,
    ) -> Records | str | None:

        return self.module.respond(

            context=context,
            records=records,
            **kwargs,

        )
