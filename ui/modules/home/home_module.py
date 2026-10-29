"""Módulo Home."""

from __future__ import annotations

from shared.records import Records

from services.home.home_service import HomeService

from ui.components.modules.assets import (
    AssetRegistry,
)

from ui.components.modules.module import (
    Module,
    ModuleDefinition,
)

from ui.modules.home.assets.create_password import (
    CreatePasswordAsset,
)

from ui.modules.home.assets.homepage import (
    HomePageAsset,
)

from ui.modules.home.assets.login import (
    LoginAsset,
)

from ui.modules.home.assets.password import (
    PasswordAsset,
)


class HomeModule:

    def __init__(self):

        self.module = Module(

            definition=ModuleDefinition(

                key="home",

                title="📥 Cadastra.me",

                navigator=False,

            ),

            service=HomeService(),

            assets=AssetRegistry(

                LoginAsset(

                    order=1,

                ),

                PasswordAsset(

                    order=2,

                ),

                CreatePasswordAsset(

                    order=3,

                ),

                HomePageAsset(

                    order=4,

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