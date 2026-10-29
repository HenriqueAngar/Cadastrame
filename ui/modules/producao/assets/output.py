"""Asset para informe de produção."""

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


class OutputAsset(Asset):

    DEFINITION = FormDefinition(

        key="output",

        title="Informe Produção",

        label="Informe Produção",

        resource_id=5,

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
                label="Cod. OP",
                type=ColumnType.NUMBER,
            ),

            "codproduto": Column(
                label="Cod. Produto",
                type=ColumnType.NUMBER,
            ),

            "linha": Column(
                label="Linha",
            ),

            "producao": Column(
                label="Produção (kg)",
                type=ColumnType.NUMBER,
            ),

            "reprocesso": Column(
                label="Reprocesso (kg)",
                type=ColumnType.NUMBER,
            ),

            "motivoreprocesso": Column(
                label="Motivo Reprocesso",
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
            # OP / PRODUTO
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

                    placeholder="Pesquise a ordem de produção",

                )

            with col2:

                codproduto = SearchInput(

                    schema="pdgeral",

                    table="produtos",

                    key_field="idproduto",

                    code_field="codproduto",

                    description_field="nomeproduto",

                    params={
                        "tipoproduto": "PRODUTO ELABORADO",
                        "marcaproduto": ["GREEN PAWS","SEVEN PETS","P.ESP. MANDALA","MANDALA",],
                    },

                ).render(

                    label="Produto",

                    key="codproduto",

                    placeholder="Pesquise o código ou nome do produto",

                )

            # ==================================================
            # LINHA
            # ==================================================

            linha = st.selectbox(

                "Linha",

                [

                    "Andritz",

                    "Ferraz",

                ],

            )

            # ==================================================
            # PRODUÇÃO / REPROCESSO
            # ==================================================

            col1, col2 = st.columns(2)

            with col1:

                producao = DecimalInput().render(

                    label="Produção (kg)",

                    key="producao",

                )

            with col2:

                reprocesso = DecimalInput().render(

                    label="Reprocesso (kg)",

                    key="reprocesso",

                )

            # ==================================================
            # MOTIVO REPROCESSO
            # ==================================================

            motivoreprocesso = SearchInput(

                schema="srcproducao",

                table="cadoutput",

                key_field="motivoreprocesso",

                description_field="motivoreprocesso",

            ).render(

                label="Motivo do Reprocesso",

                key="motivoreprocesso",

                allow_new=True,

                placeholder=(
                    "Selecione ou informe o motivo do reprocesso"
                ),

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

        if not producao.valid:

            st.error(

                producao.message,

            )

            return None

        if not reprocesso.valid:

            st.error(

                reprocesso.message,

            )

            return None

        if (
            reprocesso.value > 0
            and (
                motivoreprocesso is None
                or not str(motivoreprocesso).strip()
            )
        ):

            st.error(

                "Informe o motivo do reprocesso.",

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

                "producao": producao.value,

                "reprocesso": reprocesso.value,

                "motivoreprocesso": (

                    str(
                        motivoreprocesso
                    ).strip()

                    if motivoreprocesso is not None

                    else None

                ),

            }

        )

        return records