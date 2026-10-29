"""Asset da página inicial."""

from __future__ import annotations

import streamlit as st

from shared.records import Records

from ui.components.form.form import FormDefinition
from ui.components.modules.assets import Asset


class HomePageAsset(Asset):

    DEFINITION = FormDefinition(

        key="homepage",

        title="Bem-vindo",

        label="Página Inicial",

        resource_id=1,

    )

    def __init__(
        self, 
        *,
        order: int = 0,
    ) -> None:

        super().__init__(

            editor=False,
            order=order,

        )

    # ==========================================================
    # FORM
    # ==========================================================

    def render_form(
        self,
        *,
        context: Records | None = None,
        records: Records | None = None,
        username: str,
        modules,
        **kwargs,
    ) -> str | None:

        st.subheader(

            f"Bem-vindo, {username}!",

        )

        st.write(

            "Selecione um módulo para começar.",

        )

        st.divider()

        for module in modules:

            if module.key == "home":

                continue

            if st.button(

                module.label,

                key=f"home:{module.key}",

                use_container_width=False,

            ):

                return module.key

        return None