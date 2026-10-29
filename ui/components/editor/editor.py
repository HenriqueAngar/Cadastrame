"""Editor de registros pendentes."""

from __future__ import annotations

from collections.abc import Callable
from enum import Enum

import streamlit as st

from shared.records import (
    ColumnType,
    Records,
)


class EditorAction(Enum):

    NONE = "none"

    SUBMIT = "submit"


class Editor:
    """
    Componente responsável por renderizar
    o buffer de registros.

        • Exibir registros

        • Permitir edição

        • Solicitar confirmação

        • Informar envio
    """

    def __init__(
        self,
        title: str = "📋 Registros pendentes",
        confirmation: str = (
            "Confirmo que desejo enviar os registros."
        ),
        submit_label: str = "📤 Enviar registros",
        key: str = "editor",
    ):

        self._title = title
        self._confirmation = confirmation
        self._submit_label = submit_label
        self._key = key

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def render(
        self,
        records: Records,
        *,
        submitted: bool = False,
        validator: Callable[[Records], list[str]] | None = None,
    ) -> EditorAction:

        st.subheader(

            self._title,

        )

        if records.empty:

            st.info(

                "Nenhum registro pendente.",

            )

            return EditorAction.NONE

        if submitted:

            self.render_success()

        edited = st.data_editor(

            records.to_dataframe(),

            key=self._key,

            hide_index=True,

            width="stretch",

            num_rows="dynamic",

            disabled=self._disabled(

                records,

            ),

            column_config=self._column_config(

                records,

            ),

        )

        records.from_dataframe(

            edited,

        )

        errors = (
            validator(records)
            if validator is not None
            else records.validate()
        )

        for error in errors:

            st.error(error)

        confirmed = st.checkbox(

            self._confirmation,

            key=f"{self._key}:confirmation",

        )

        if st.button(

            self._submit_label,

            key=f"{self._key}:submit",

            width="stretch",

            disabled=not confirmed or bool(errors),

        ):

            return EditorAction.SUBMIT

        return EditorAction.NONE

    def render_success(
        self,
    ) -> None:

        st.success(

            "Registros enviados com sucesso.",

        )

    # ==========================================================
    # PRIVATE
    # ==========================================================

    @staticmethod
    def _disabled(
        records: Records,
    ) -> list[str]:

        return [

            name

            for name, column in records.columns.items()

            if not column.editable

        ]

    @staticmethod
    def _column_config(
        records: Records,
    ) -> dict:

        config = {}

        for name, column in records.columns.items():

            if column.type is ColumnType.NUMBER:

                config[name] = st.column_config.NumberColumn(

                    label=column.label or name,

                    width=column.width,

                    format=column.format,

                )

            elif column.type is ColumnType.DATE:

                config[name] = st.column_config.DateColumn(

                    label=column.label or name,

                    width=column.width,

                    format=column.format or "DD/MM/YYYY",

                )

            elif column.type is ColumnType.DATETIME:

                config[name] = st.column_config.DatetimeColumn(

                    label=column.label or name,

                    width=column.width,

                    format=column.format or "DD/MM/YYYY HH:mm",

                    step=60,

                )

            else:

                config[name] = st.column_config.Column(

                    label=column.label or name,

                    width=column.width,

                )

        return config
