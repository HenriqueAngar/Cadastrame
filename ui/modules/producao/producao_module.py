"""Módulo Produção."""

from __future__ import annotations

from shared.records import Records

from services.producao.producao_service import (
    ProducaoService,
)

from ui.components.modules.assets import (
    AssetRegistry,
)

from ui.components.modules.module import (
    Module,
    ModuleDefinition,
)

from ui.modules.producao.assets.ensaque import (
    EnsaqueAsset,
)

from ui.modules.producao.assets.paradas import (
    ParadasAsset,
)

from ui.modules.producao.assets.output import (
    OutputAsset,
)


class ProducaoModule:

    def __init__(self):

        self.module = Module(

            definition=ModuleDefinition(

                key="producao",

                title="🏭 Produção",

            ),

            service=ProducaoService(),

            assets=AssetRegistry(

                EnsaqueAsset(

                    order=1,

                ),

                ParadasAsset(

                    order=2,

                ),

                OutputAsset(

                    order=3,

                ),

            ),

        )

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