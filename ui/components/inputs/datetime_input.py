"""Componente para entrada combinada de data e hora."""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from shared.parser import (
    ParseResult,
    Parser,
)


class DateTimeInput:
    """Entrada textual de data e hora em um único campo."""

    def render(
        self,
        label: str,
        key: str,
        value: datetime | None = None,
        placeholder: str = "DD/MM/AAAA HH:MM",
    ) -> ParseResult[datetime]:

        default = (
            value
            or datetime.now().replace(
                second=0,
                microsecond=0,
            )
        )

        text = st.text_input(
            label=label,
            value=default.strftime(
                "%d/%m/%Y %H:%M",
            ),
            key=key,
            placeholder=placeholder,
            help="Informe no formato DD/MM/AAAA HH:MM.",
        )

        return Parser.datetime(
            text,
        )
