"""Asset para autenticação do usuário."""

from __future__ import annotations

import streamlit as st

from shared.records import (
    Column,
    Records,
)

from domain.home.password import Password

from ui.components.form.form import FormDefinition
from ui.components.modules.assets import Asset


class PasswordAsset(Asset):

    DEFINITION = FormDefinition(

        key="password",

        title="Entrar",

        label="Senha",

        resource_id=1,

        columns={

            "email": Column(),

            "password": Column(

                label="Senha",

            ),

        },

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
        **kwargs,
    ) -> Records | None:

        email = ""

        if context is not None and context.data:

            email = context.data[0].email

        with st.form(

            self.definition.form_key,

            clear_on_submit=True,

        ):

            st.subheader(

                self.definition.title,

            )

            password = st.text_input(

                "Senha",

                type="password",

                placeholder="Informe sua senha",

            )

            submitted = st.form_submit_button(

                "Entrar",

                use_container_width=True,

            )

        if not submitted:

            return None

        assert records is not None

        records.clear()

        records.metadata["key"] = "login"

        records.add(

            {

                "email": email,

                "password": password,

            }

        )


        return records