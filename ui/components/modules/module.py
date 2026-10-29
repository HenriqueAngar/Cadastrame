"""Componente base para módulos."""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)

import streamlit as st

from services.base_service import Service

from shared.records import Records

from ui.components.modules.assets import (
    AssetRegistry,
)

from ui.components.modules.navigator import (
    FormNavigator,
)


# ==========================================================
# DEFINITION
# ==========================================================

@dataclass(slots=True, frozen=True)
class ModuleDefinition:
    """
    Definição declarativa de um módulo.
    """

    key: str

    title: str

    navigator: bool = True


# ==========================================================
# MODULE
# ==========================================================

@dataclass(slots=True)
class Module:
    """
    Componente base para módulos.

    Responsabilidades

        • Determinar os assets disponíveis

        • Controlar a navegação entre assets

        • Associar o contrato do asset aos registros

        • Encaminhar registros ao serviço
    """

    definition: ModuleDefinition

    assets: AssetRegistry

    service: Service

    navigator: FormNavigator = field(
        init=False,
    )

    def __post_init__(
        self,
    ) -> None:

        self.navigator = FormNavigator(

            key=self.definition.key,

        )

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def respond(
        self,
        *,
        context: Records | None = None,
        records: Records | None = None,
        resources: set[int] | None = None,
        authenticated: bool = False,
        **kwargs,
    ) -> Records | str | None:

        assets = self.service.allowed(

            self.assets,

            context,

            resources=resources or set(),

            authenticated=authenticated,

        )

        if not assets:

            st.info(

                "Nenhum formulário disponível.",

            )

            return None

        st.title(

            self.definition.title,

        )

        # ======================================================
        # NAVIGATION
        # ======================================================

        if self.definition.navigator:

            navigation = self.navigator.render(

                assets,

            )

            asset = navigation.asset

            # ==================================================
            # ASSET CHANGE
            # ==================================================

            if navigation.changed:

                if records is not None:

                    records.clear()

                st.rerun()

            st.divider()

        else:

            asset = assets[0]

        # ======================================================
        # RECORD CONTRACT
        # ======================================================

        if records is None:

            records = Records(

                columns=asset.definition.columns,

            )

        else:

            records.columns = asset.definition.columns

        # ======================================================
        # ASSET
        # ======================================================

        response = asset.respond(

            context=context,

            records=records,

            submitted=self.navigator.submitted,

            **kwargs,

        )

        if response is None:

            return None

        if isinstance(

            response,

            str,

        ):

            return response

        # ======================================================
        # SERVICE
        # ======================================================

        result = self.service.process(

            asset.definition.key,

            response,

        )

        self.navigator.submitted = True

        return result
