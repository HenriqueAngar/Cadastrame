"""Asset para criação da senha de acesso."""

from __future__ import annotations

import streamlit as st

from shared.records import (
    Column,
    Records,
)

from domain.home.password import Password

from ui.components.modules.assets import Asset
from ui.components.form.form import FormDefinition


class CreatePasswordAsset(Asset):

    DEFINITION = FormDefinition(

        key="create_password",

        title="Criar senha",

        label="Primeiro acesso",

        resource_id=1,

        columns={

            "email": Column(),

            "password": Column(

                label="Senha",

            ),

            "confirmation": Column(

                label="Confirmação",

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

            clear_on_submit=False,

        ):

            st.subheader(

                self.definition.title,

            )

            password = st.text_input(

                "Nova senha",

                type="password",

                placeholder="Informe sua senha",

            )

            confirmation = st.text_input(

                "Confirmar senha",

                type="password",

                placeholder="Repita sua senha",

            )

            submitted = st.form_submit_button(

                "Criar senha",

                use_container_width=True,

            )

        if not submitted:

            return None

        assert records is not None

        records.clear()

        records.metadata["key"] = "create_password"

        records.add(

            {

                "email": email,

                "password": password,

                "confirmation": confirmation,

            }

        )

        return records