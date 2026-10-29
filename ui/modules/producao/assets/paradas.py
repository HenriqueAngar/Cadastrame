"""Asset para registro de paradas."""

from __future__ import annotations

from datetime import (
    datetime,
    timedelta,
)

import streamlit as st

from shared.records import (
    Column,
    ColumnType,
    Records,
)

from ui.components.form.form import (
    FormDefinition,
)

from ui.components.inputs.search_input import (
    SearchInput,
)

from ui.components.inputs.datetime_input import (
    DateTimeInput,
)

from ui.components.modules.assets import (
    Asset,
)


class ParadasAsset(Asset):

    DEFINITION = FormDefinition(

        key="paradas",

        title="Registro de Paradas",

        label="Registro de Paradas",

        resource_id=7,

        columns={

            "datahorainicio": Column(
                label="Data/Hora Início",
                type=ColumnType.DATETIME,
                editable=True,
                format="DD/MM/YYYY HH:mm",
            ),

            "datahorafim": Column(
                label="Data/Hora Fim",
                type=ColumnType.DATETIME,
                editable=True,
                format="DD/MM/YYYY HH:mm",
            ),

            "linha": Column(
                label="Linha",
            ),

            "tipoparada": Column(
                label="Tipo da Parada",
            ),

            "motivoparada": Column(
                label="Motivo da Parada",
            ),

            "observacao": Column(
                label="Observação",
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

    def validate_records(
        self,
        records: Records,
    ) -> list[str]:

        errors = super().validate_records(

            records,

        )

        for index, record in enumerate(
            records.data,
            start=1,
        ):

            inicio = record.get(
                "datahorainicio",
            )

            fim = record.get(
                "datahorafim",
            )

            if not isinstance(inicio, datetime):

                continue

            if not isinstance(fim, datetime):

                continue

            if fim <= inicio:

                errors.append(
                    f"Registro {index}: a data/hora final deve "
                    "ser posterior à inicial."
                )

        return errors

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
            # DATA / HORA
            # ==================================================

            col1, col2 = st.columns(2)

            agora = datetime.now().replace(
                second=0,
                microsecond=0,
            )

            with col1:

                inicio = DateTimeInput().render(

                    label="Data/Hora Início",

                    key="paradas_datahorainicio",

                    value=agora,

                )

            with col2:

                fim = DateTimeInput().render(

                    label="Data/Hora Fim",

                    key="paradas_datahorafim",

                    value=agora + timedelta(
                        minutes=15,
                    ),

                )

            # ==================================================
            # CLASSIFICAÇÃO
            # ==================================================

            col1, col2 = st.columns(2)

            with col1:

                linha = st.selectbox(

                    "Linha",

                    [
                        "Andritz",
                        "Ferraz",
                    ],

                )

            with col2:

                tipoparada = st.selectbox(

                    "Tipo da Parada",

                    [
                        "Set-up",
                        "Entupimento",
                        "Manutenção Mecânica",
                        "Manutenção Elétrica",
                        "Tanques de Multipartículas Cheios",
                        "Calibração Balança",
                        "Falta de Mistura",
                        "Parada Programada",
                        "Ineficiência de Moagem",
                        "Início e Final de Turno",
                        "Falta de Vapor",
                        "Teste",
                        "Troca de Navalhas/Bracinhos",
                        "Produto Fora do Padrão",
                        "Falta de Matéria Prima Dosagem",
                        "Outros",
                    ],

                )

            # ==================================================
            # MOTIVO
            # ==================================================

            motivoparada = SearchInput(

                schema="srcproducao",

                table="cadparadas",

                key_field="motivoparada",

                description_field="motivoparada",

            ).render(

                label="Motivo da Parada",

                key="motivoparada",

                allow_new=True,

                placeholder=(
                    "Selecione ou informe um motivo"
                ),

            )

            # ==================================================
            # OBSERVAÇÃO
            # ==================================================

            observacao = st.text_area(

                "Observação",

                placeholder=(
                    "Informe detalhes adicionais da parada"
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

        if (
            motivoparada is None
            or not str(motivoparada).strip()
        ):

            st.error(

                "Informe o motivo da parada.",

            )

            return None

        if not inicio.valid:

            st.error(inicio.message)

        if not fim.valid:

            st.error(fim.message)

        if not inicio.valid or not fim.valid:

            return None

        assert inicio.value is not None
        assert fim.value is not None

        datahorainicio = inicio.value

        datahorafim = fim.value

        if datahorafim <= datahorainicio:

            st.error(

                "A data/hora final deve ser posterior "
                "à data/hora inicial.",

            )

            return None

        records.add(

            {

                "datahorainicio": datahorainicio,

                "datahorafim": datahorafim,

                "linha": linha,

                "tipoparada": tipoparada,

                "motivoparada": str(
                    motivoparada
                ).strip(),

                "observacao": observacao.strip(),

            }

        )

        return records
