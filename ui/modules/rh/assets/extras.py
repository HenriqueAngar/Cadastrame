"""Asset do cadastro manual de extras de folha."""

from __future__ import annotations

from datetime import date, timedelta

import streamlit as st

from domain.rh.extras import Extras
from repositories.rh.rh_repository import RHRepository
from shared.records import Column, ColumnType, Records
from ui.components.form.form import FormDefinition
from ui.components.inputs.decimal_input import DecimalInput
from ui.components.modules.assets import Asset


class ExtrasAsset(Asset):

    MESES = (
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
    )

    @staticmethod
    def competencia_padrao(hoje: date) -> date:
        return (hoje.replace(day=1) - timedelta(days=1)).replace(day=1)


    DEFINITION = FormDefinition(

        key="extras",

        title="⏱️ Cadastro de Extras de Folha",

        label="Extras de Folha",

        resource_id=8,

        # A data de criação é gerada pelo banco, fora dos dados de entrada.
        columns={

            "idextra": Column(
                label="ID do extra",
                type=ColumnType.NUMBER,
            ),

            "idcolaborador": Column(
                label="ID do colaborador",
                type=ColumnType.NUMBER,
            ),

            "idcentrocusto": Column(
                label="ID do centro de custo",
                type=ColumnType.NUMBER,
            ),

            "codigocentrocusto": Column(
                label="Código do centro de custo",
                type=ColumnType.NUMBER,
            ),

            "competencia": Column(
                label="Competência",
                type=ColumnType.DATE,
            ),

            "horasextras": Column(
                label="Horas extras",
                editable=True,
                type=ColumnType.NUMBER,
            ),

            "valoresextras": Column(
                label="Valor extra",
                editable=True,
                type=ColumnType.NUMBER,
                format="R$ %.2f",
            ),

            "observacao": Column(
                label="Observação",
                editable=True,
            ),

        },

    )

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

            clear_on_submit=False,

        ):

            st.subheader(self.definition.title)

            colaboradores = RHRepository().list_colaboradores_extras()
            colaborador = st.selectbox(
                "Colaborador",
                options=colaboradores,
                index=None,
                format_func=lambda item: f"{item[0]} - {item[1]}",
                key="extras_colaborador",
                placeholder="Pesquise o ID ou nome do colaborador",
            )
            idcolaborador = None if colaborador is None else colaborador[0]

            hoje = date.today()
            padrao = self.competencia_padrao(hoje)
            col_mes, col_ano = st.columns(2)

            with col_mes:
                mes = st.selectbox(
                    "Mês de competência",
                    options=range(1, 13),
                    index=padrao.month - 1,
                    format_func=lambda numero: self.MESES[numero - 1],
                    key="extras_mes_competencia",
                )

            with col_ano:
                anos = list(range(hoje.year, 1999, -1))
                ano = st.selectbox(
                    "Ano de competência",
                    options=anos,
                    index=anos.index(padrao.year),
                    key="extras_ano_competencia",
                )

            competencia = date(ano, mes, 1)

            col1, col2 = st.columns(2)

            with col1:

                horasextras = DecimalInput().render(

                    label="Horas extras",
                    key="extras_horas",

                )

            with col2:

                valoresextras = DecimalInput().render(

                    label="Valor extra",
                    key="extras_valor",

                )

            observacao = st.text_area(

                "Observação",
                key="extras_observacao",

            )

            submitted = st.form_submit_button(

                "➕ Adicionar",
                use_container_width=False,

            )

        if not submitted:

            return None

        if idcolaborador is None:

            st.error("Informe um colaborador.")

            return None

        if not horasextras.valid:

            st.error(horasextras.message)

            return None

        if not valoresextras.valid:

            st.error(valoresextras.message)

            return None

        candidato = Records(data=[{
            "idcolaborador": int(idcolaborador),
            "competencia": competencia,
            "horasextras": horasextras.value,
            "valoresextras": valoresextras.value,
            "observacao": observacao.strip() or None,
        }])

        try:
            Extras(repository=RHRepository()).identificar(candidato)
        except ValueError as error:
            st.error(str(error))
            return None

        records.add(candidato.data[0])

        return records
