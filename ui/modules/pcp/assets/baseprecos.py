"""Asset para cadastro de preços."""

from __future__ import annotations

from datetime import date

import streamlit as st

from shared.records import (
    Column,
    ColumnType,
    Records,
)

from ui.components.form.form import (
    FormDefinition,
)

from ui.components.inputs.decimal_input import (
    DecimalInput,
)

from ui.components.modules.assets import (
    Asset,
)


class BasePrecosAsset(Asset):

    DEFINITION = FormDefinition(

        key="baseprecos",

        title="💲 Cadastro de Preço de Produtos",

        label="Preço de Produtos",

        resource_id=4,

        columns={

            "codproduto": Column(
                label="Código do Produto",
                editable=True,
                type=ColumnType.NUMBER,
            ),

            "datainicio": Column(
                label="Data Inicial",
                type=ColumnType.DATE,
            ),

            "datafim": Column(
                label="Data Final",
                type=ColumnType.DATE,
            ),

            "preco": Column(
                label="Preço",
                editable=True,
                type=ColumnType.NUMBER,
            ),
},

    )

    def __init__(
        self,
        *,
        order: int = 0,
    ) -> None:

        super().__init__(

            order=order,

        )

        print(f"Asset {id(self)}")

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

        assert records is not None

        with st.form(

            self.definition.form_key,

            clear_on_submit=True,

        ):

            st.subheader(

                self.definition.title,

            )

            codproduto, ano, preco = self._inputs()

            submitted = st.form_submit_button(

                "➕ Adicionar",

                use_container_width=False,

            )

        if not submitted:

            return None

        if not preco.valid:

            st.error(

                preco.message,

            )

            return None
        
        print(f"[ASSET BEFORE] id={id(records)} size={len(records)}")

        records.add(

            self._record(

                codproduto,

                ano,

                preco.value,

            )

        )

        print(f"[ASSET AFTER] id={id(records)} size={len(records)}")

        return records

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _inputs(
        self,
    ):

        col1, col2, col3 = st.columns(

            3,

        )

        with col1:

            codproduto = st.number_input(

                "Código do Produto",

                min_value=1,

                step=1,

                value=1,

            )

        with col2:

            ano = st.number_input(

                "Ano de Vigência",

                min_value=2000,

                max_value=2100,

                value=date.today().year,

                step=1,

            )

        with col3:

            preco = DecimalInput().render(

                label="Preço",

                key="preco",

            )

        return codproduto, ano, preco

    @staticmethod
    def _record(
        codproduto: int,
        ano: int,
        preco: float,
    ) -> dict:

        return {

            "codproduto": codproduto,

            "datainicio": date(

                ano,

                1,

                1,

            ),

            "datafim": date(

                ano,

                12,

                31,

            ),

            "preco": preco,

        }
