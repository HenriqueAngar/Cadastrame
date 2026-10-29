"""Asset para identificação do usuário."""

from __future__ import annotations

import streamlit as st

from shared.records import (
    Column,
    Records,
)

from ui.components.form.form import FormDefinition
from ui.components.modules.assets import Asset


class LoginAsset(Asset):

    DEFINITION = FormDefinition(

        key="login",

        title="Entrar",

        label="Entrar",

        resource_id=1,

        columns={

            "email": Column(

                label="E-mail",

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

        with st.form(

            self.definition.form_key,

            clear_on_submit=False,

        ):

            st.subheader(

                self.definition.title,

            )

            email = st.text_input(

                "E-mail",

                placeholder="usuario@empresa.com",

            )

            submitted = st.form_submit_button(

                "Continuar",

                use_container_width=True,

            )

        if not submitted:

            return None

        assert records is not None

        records.clear()

        records.metadata["key"] = "identify"

        records.add(

            {

                "email": email.strip().lower(),

            }

        )

        return records