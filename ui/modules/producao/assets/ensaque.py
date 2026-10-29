"""Asset para informe de ensaques."""

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

from ui.components.inputs.search_input import (
    SearchInput,
)

from ui.components.modules.assets import (
    Asset,
)


class EnsaqueAsset(Asset):

    DEFINITION = FormDefinition(

        key="ensaques",

        title="Informe de Ensaques",

        label="Informe de Ensaques",

        resource_id=6,

        columns={

            "data": Column(
                label="Data",
                type=ColumnType.DATE,
            ),

            "turno": Column(
                label="Turno",
                type=ColumnType.NUMBER,
            ),

            "codop": Column(
                label="Ordem Produção",
                type=ColumnType.NUMBER,
            ),

            "codproduto": Column(
                label="Código Produto",
                type=ColumnType.NUMBER,
            ),

            "nomeproduto": Column(
                label="Nome Produto",
            ),

            "linha": Column(
                label="Máquina",
            ),

            "quantidade": Column(
                label="Quantidade",
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

            # ==================================================
            # DATA / TURNO
            # ==================================================

            col1, col2 = st.columns(2)

            with col1:

                data = st.date_input(

                    "Data",

                    value=date.today(),

                    format="DD/MM/YYYY",

                )

            with col2:

                turno = st.selectbox(

                    "Turno",

                    [1, 2, 3],

                )

            # ==================================================
            # OP / LINHA
            # ==================================================

            col1, col2 = st.columns(2)

            with col1:

                codop = SearchInput(

                    schema="pdestoque",

                    table="ordensproducao",

                    key_field="idordemproducao",

                    description_field="codordemproducao",

                ).render(

                    label="Ordem de Produção",

                    key="codop",

                    placeholder=(
                        "Pesquise a ordem de produção"
                    ),

                )

            with col2:

                linha = st.selectbox(

                    "Linha",

                    [
                        "Andritz",
                        "Ferraz",
                    ],

                )

            # ==================================================
            # PRODUTO / QUANTIDADE
            # ==================================================

            col1, col2 = st.columns(2)

            with col1:

                codproduto = SearchInput(

                    schema="pdgeral",

                    table="produtos",

                    key_field="idproduto",

                    code_field="codproduto",

                    description_field="nomeproduto",

                    params={
                        "tipoproduto": ("PRODUTO ACABADO"),
                        "marcaproduto": ["GREEN PAWS","SEVEN PETS","P.ESP. MANDALA", "MANDALA",],
                        "grupoproduto": ["RACAO DOG - WMW", "RACAO GATO - WMW"]
                    },

                ).render(

                    label="Produto",

                    key="codproduto",

                    placeholder=(
                        "Pesquise o código ou nome do produto"
                    ),

                )

            with col2:

                quantidade = DecimalInput().render(

                    label="Quantidade Unidades",

                    key="quantidade",

                )

            submitted = st.form_submit_button(

                "➕ Adicionar",

                use_container_width=False,

            )

        # ======================================================
        # SUBMIT
        # ======================================================

        if not submitted:

            return None

        # ======================================================
        # VALIDATION
        # ======================================================

        if codop is None:

            st.error(

                "Informe a ordem de produção.",

            )

            return None

        if codproduto is None:

            st.error(

                "Informe o produto.",

            )

            return None

        if not quantidade.valid:

            st.error(

                quantidade.message,

            )

            return None

        # ======================================================
        # RECORD
        # ======================================================

        records.add(

            {

                "data": data,

                "turno": turno,

                "codop": codop,

                "codproduto": codproduto,

                "linha": linha,

                "quantidade": quantidade.value,

            }

        )

        return records