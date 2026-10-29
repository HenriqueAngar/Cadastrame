"""Módulo PCP."""

from __future__ import annotations

from shared.records import Records

from services.pcp.pcp_service import (
    BasePrecosService,
)

from ui.components.modules.assets import (
    AssetRegistry,
)

from ui.components.modules.module import (
    Module,
    ModuleDefinition,
)

from ui.modules.pcp.assets.baseprecos import (
    BasePrecosAsset,
)


class PCPModule:

    def __init__(self):

        self.module = Module(

            definition=ModuleDefinition(

                key="pcp",

                title="📋 PCP",

            ),

            service=BasePrecosService(),

            assets=AssetRegistry(

                BasePrecosAsset(

                    order=1,

                ),

            ),

        )

        print(f"PCPModule {id(self)}")

    # ==========================================================
    # PUBLIC
    # ==========================================================

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